from concurrent.futures import CancelledError
from datetime import datetime
import threading
import logging
import asyncio
import time

from yarl import URL

from lona.exceptions import StopReason, ServerStop, UserAbort
from lona.html.abstract_node import AbstractNode
from lona.html.document import Document
from lona.input_event import InputEvent
from lona.request import Request
from lona.types import Symbol

from lona.protocol import (
    encode_http_redirect,
    encode_view_start,
    encode_view_stop,
    encode_redirect,
    encode_data,
)


logger = logging.getLogger('lona.view_runtime')


class ViewRuntime:
    class STATE(Symbol):
        NOT_STARTED = Symbol('NOT_STARTED', 10)

        RUNNING = Symbol('RUNNING', 21)
        WAITING_FOR_IOLOOP = Symbol('WAITING_FOR_IOLOOP', 22)
        SLEEPING = Symbol('SLEEPING', 23)
        WAITING_FOR_INPUT = Symbol('WAITING_FOR_INPUT', 24)

        FINISHED = Symbol('FINISHED', 31)
        CRASHED = Symbol('CRASHED', 32)
        STOPPED_BY_USER = Symbol('STOPPED_BY_USER', 33)
        STOPPED_BY_SERVER = Symbol('STOPPED_BY_SERVER', 34)

    def __init__(self, server, url, route, match_info, post_data={},
                 frontend=False, start_connection=None):

        self.server = server
        self.url = URL(url or '')
        self.route = route
        self.match_info = match_info
        self.post_data = post_data
        self.frontend = frontend
        self.start_connection = start_connection

        # find view
        if route:
            self.view = route.view

        else:
            self.view = self.server.settings.ERROR_404_HANDLER

        if frontend:
            self.view = self.server.settings.FRONTEND_VIEW

            if route and route.frontend_view:
                self.view = route.frontend_view

        self.view_spec, self.view = self.server.view_loader.load(self.view)
        self.name = repr(self.view)

        if self.view_spec.is_class_based:
            self.view = self.view()

        # setup state
        self.connections = {}
        # contains: {
        #     connection: (window_id, url),
        # }

        self.document = Document()

        self.stopped = asyncio.Future(loop=self.server.loop)
        self.is_stopped = False
        self.stop_reason = None
        self.is_daemon = False

        self.view_runtime_id = time.monotonic_ns()
        self.state = self.STATE.NOT_STARTED
        self.thread_ident = None
        self.started_at = None
        self.stopped_at = None

        self.pending_input_events = {
            'event': None,
            'click': None,
            'change': None,
            'submit': None,
        }

        self.request = Request(
            view_runtime=self,
            connection=self.start_connection,
        )

        self.view_args = (self.request,)
        self.view_kwargs = {}

        if not self.frontend:
            self.view_kwargs = dict(self.match_info or {})

    # state ###################################################################
    @property
    def state(self):
        if self.is_stopped:
            if self.stop_reason is not None:
                if isinstance(self.stop_reason, UserAbort):
                    return self.STATE.STOPPED_BY_USER

                elif isinstance(self.stop_reason, ServerStop):
                    return self.STATE.STOPPED_BY_SERVER

                else:
                    return self.STATE.CRASHED

            else:
                return self.STATE.FINISHED

        return self._state

    @state.setter
    def state(self, new_state):
        self._state = new_state

    # middlewares #############################################################
    def run_middlewares(self):
        try:
            handled, raw_response_dict, middleware = \
                self.server.middleware_controller.process_request(
                    view=self.view,
                    request=self.request,
                )

            if handled:
                if not raw_response_dict:
                    raw_response_dict = ''

                self.send_view_start()

                response_dict = self.handle_raw_response_dict(
                    raw_response_dict,
                )

                self.send_view_stop()

                return response_dict

        except Exception as exception:
            logger.error(
                'Exception raised while running middleware hooks',
                exc_info=True,
            )

            view_spec, view = self.server.view_loader.load(
                self.server.settings.ERROR_500_HANDLER,
            )

            return self.handle_raw_response_dict(
                view(
                    self.request,
                    exception,
                )
            )

    # start and stop ##########################################################
    def start(self):
        try:
            # update internal state
            self.thread_ident = threading.current_thread().ident
            self.state = self.STATE.RUNNING
            self.started_at = datetime.now()

            # start view
            self.send_view_start()

            if self.view_spec.is_class_based:
                raw_response_dict = self.view.handle_request(
                    *self.view_args,
                    **self.view_kwargs,
                )

            else:
                raw_response_dict = self.view(
                    *self.view_args,
                    **self.view_kwargs,
                )

            # response dicts
            if raw_response_dict:
                if isinstance(raw_response_dict, AbstractNode):
                    self.request.client.show(html=raw_response_dict)

                    return

                # check if non-interactive features got used in
                # interactive mode
                if(self.route and self.route.interactive and
                    isinstance(raw_response_dict, dict) and (
                     'json' in raw_response_dict or
                     'file' in raw_response_dict)):

                    raise RuntimeError('JSON and file responses are only available in non-interactive mode')  # NOQA

                return self.handle_raw_response_dict(raw_response_dict)

        except(StopReason, CancelledError):
            pass

        except Exception as exception:
            self.stop_reason = exception

            logger.error(
                'Exception raised while running %s',
                self.view,
                exc_info=True,
            )

            view_spec, view = self.server.view_loader.load(
                self.server.settings.ERROR_500_HANDLER,
            )

            return self.handle_raw_response_dict(
                view(
                    self.request,
                    exception,
                )
            )

        finally:
            self.is_stopped = True
            self.stopped_at = datetime.now()
            self.send_view_stop()

    def stop(self, reason=UserAbort, clean_up=True):
        self.stop_reason = reason

        if not isinstance(self.stop_reason, Exception):
            self.stop_reason = self.stop_reason()

        # let all calls on request.view.await_sync() crash with
        # the set stop reason
        def _set_stopped():
            if not self.stopped.done():
                self.stopped.set_result(True)

        self.server.loop.call_soon_threadsafe(_set_stopped)

        # cancel all pending user input events
        for pending_input_event in self.pending_input_events.copy().items():
            if not pending_input_event[1]:
                continue

            name, (future, nodes) = pending_input_event

            if not future.done():
                future.set_exception(self.stop_reason)

        # clean up
        if clean_up:
            # drop all connections
            self.connections = {}

            # multi user views have no start_connection
            if self.start_connection:
                self.server.view_runtime_controller.remove_view_runtime(self)

    def issue_500_error(self, exception):
        # stop the runtime but don't run cleanup code to get the
        # output of the 500 handle through
        self.stop(reason=exception, clean_up=False)

        # run 500 handler
        # this runs if the crash happened in an input event handler after
        # the view stopped
        if self.is_stopped:
            view_spec, view = self.server.view_loader.load(
                self.server.settings.ERROR_500_HANDLER,
            )

            self.handle_raw_response_dict(
                view(
                    self.request,
                    exception,
                )
            )

            logger.error(
                'Exception raised after running %s',
                self.view,
                exc_info=True,
            )

    # connection management ###################################################
    def add_connection(self, connection, window_id, url):
        self.connections[connection] = (window_id, url, )

        with self.document.lock:
            data_type, data = self.document.serialize()

            if not data:
                return

            self.send_data(
                data=[data_type, data],
                connections={connection: (window_id, url, )},
            )

    def reconnect_connection(self, connection, window_id, url):
        self.connections[connection] = (window_id, url, )

        with self.document.lock:
            self.send_view_start()

            data_type, data = self.document.serialize()

            if not data:
                return

            self.send_data(
                data=[data_type, data],
                connections={connection: (window_id, url, )},
            )

    def remove_connection(self, connection, window_id=None):
        if connection in self.connections:
            if window_id:
                if self.connections[connection] == window_id:
                    self.connections.pop(connection)

            else:
                self.connections.pop(connection)

        # if the last connection gets closed and the view should
        # not continue running in background, it gets stopped
        if(not self.connections and
           not self.is_daemon and
           not self.view_spec.multi_user):

            self.stop()

    # lona messages ###########################################################
    def send_redirect(self, target_url, connections={}):
        connections = connections or self.connections

        for connection, (window_id, url) in connections.items():
            message = encode_redirect(
                window_id=window_id,
                view_runtime_id=self.view_runtime_id,
                target_url=target_url,
            )

            connection.send_str(message)

    def send_http_redirect(self, target_url, connections={}):
        connections = connections or self.connections

        for connection, (window_id, url) in connections.items():
            message = encode_http_redirect(
                window_id=window_id,
                view_runtime_id=self.view_runtime_id,
                target_url=target_url,
            )

            connection.send_str(message)

    def send_data(self, title=None, data=None, connections={}):
        connections = connections or self.connections

        # send message
        for connection, (window_id, url) in list(connections.items()):
            message = encode_data(
                window_id=window_id,
                view_runtime_id=self.view_runtime_id,
                title=title,
                data=data,
            )

            connection.send_str(message)

    def send_view_start(self, connections={}):
        connections = connections or self.connections

        for connection, (window_id, url) in list(connections.items()):
            message = encode_view_start(
                window_id=window_id,
                view_runtime_id=self.view_runtime_id,
            )

            connection.send_str(message)

    def send_view_stop(self, connections={}):
        connections = connections or self.connections

        for connection, (window_id, url) in list(connections.items()):
            message = encode_view_stop(
                window_id=window_id,
                view_runtime_id=self.view_runtime_id,
            )

            connection.send_str(message)

    def handle_raw_response_dict(self, raw_response_dict, connections={}):
        connections = connections or self.connections

        response_dict = self.server.response_parser.render_response_dict(
            raw_response_dict=raw_response_dict,
            view_name=self.name,
        )

        if response_dict['redirect']:
            self.send_redirect(
                response_dict['redirect'],
                connections=connections,
            )

        elif response_dict['http_redirect']:
            self.send_http_redirect(
                response_dict['http_redirect'],
                connections=connections,
            )

        elif response_dict['text']:
            with self.document.lock:
                data = self.document.apply(response_dict['text'])
                self.send_data(data=data, connections=connections)

        return response_dict

    # input events ############################################################
    def await_input_event(self, nodes=[], event_type='event'):
        async def _await_input_event():
            future = asyncio.Future()
            self.pending_input_events[event_type] = [future, nodes]

            return await future

        return self.server.run_coroutine_sync(_await_input_event())

    def handle_input_event(self, connection, payload):
        request = Request(
            view_runtime=self,
            connection=connection,
        )

        input_event = InputEvent(
            request=request,
            payload=payload,
            document=self.document,
        )

        def send_html_update():
            with self.document.lock:
                data = self.document.apply(self.document.html)

                if data:
                    self.send_data(data=data)

        try:
            # input event root handler (class based views)
            if self.view_spec.has_input_event_root_handler:
                input_event = self.view.handle_input_event_root(input_event)

                if not input_event:
                    send_html_update()

                    return

            # widgets
            for widget in input_event.widgets[::-1]:
                input_event = widget.handle_input_event(input_event)

                if not input_event:
                    send_html_update()

                    return

            # pending input events
            if(input_event.name in self.pending_input_events and
               self.pending_input_events[input_event.name] is not None):

                future, nodes = self.pending_input_events[input_event.name]

                if not nodes or input_event.node in nodes:
                    future.set_result(input_event)
                    self.pending_input_events[input_event.name] = None

                    return

            if self.pending_input_events['event'] is not None:
                future, nodes = self.pending_input_events['event']

                if not nodes or input_event.node in nodes:
                    future.set_result(input_event)
                    self.pending_input_events['event'] = None

                    return

            # input event handler (class based views)
            if self.view_spec.has_input_event_handler:
                input_event = self.view.handle_input_event(input_event)

                if not input_event:
                    send_html_update()

        except(StopReason, CancelledError):
            pass

        except Exception as exception:
            self.issue_500_error(exception)
