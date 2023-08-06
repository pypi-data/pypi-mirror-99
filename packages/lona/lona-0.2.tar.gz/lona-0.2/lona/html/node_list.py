from time import monotonic_ns

from lona.html.abstract_node import AbstractNode
from lona.protocol import OPERATION, PATCH_TYPE
from lona.html.text_node import TextNode


class NodeList:
    def __init__(self, node):
        self._node = node
        self._nodes = []
        self._changes = []

    # list helper #############################################################
    def _check_node(self, node):
        if isinstance(node, (str, int, float, bool, )):
            node = TextNode(node)

        if not isinstance(node, AbstractNode):
            raise ValueError('unsupported type: {}'.format(repr(node)))

        return node

    def _prepare_node(self, node):
        if node.parent and node.parent is not self._node:
            node.parent.remove(node)

        elif node == self._node.root:
            raise RuntimeError('loop detected')

        node.parent = self._node
        node._clear_changes()

    def insert(self, index, node):
        node = self._check_node(node)

        with self._node.document.lock:
            self._prepare_node(node)
            self._nodes.insert(index, node)

            index = self._nodes.index(node)

            self._changes.append([
                monotonic_ns(),
                self._node._id,
                PATCH_TYPE.NODES,
                OPERATION.INSERT,
                index,
                node._serialize(),
            ])

    def append(self, node):
        node = self._check_node(node)

        with self._node.document.lock:
            self._prepare_node(node)
            self._nodes.append(node)

            index = self._nodes.index(node)

            self._changes.append([
                monotonic_ns(),
                self._node._id,
                PATCH_TYPE.NODES,
                OPERATION.INSERT,
                index,
                node._serialize(),
            ])

    def remove(self, node):
        with self._node.document.lock:
            self._nodes.remove(node)

            node.parent = None

            self._changes.append([
                monotonic_ns(),
                self._node._id,
                PATCH_TYPE.NODES,
                OPERATION.REMOVE,
                node._id,
            ])

    def pop(self, index):
        with self._node.document.lock:
            node = self._nodes.pop(index)

            node.parent = None

            self._changes.append([
                monotonic_ns(),
                self._node._id,
                PATCH_TYPE.NODES,
                OPERATION.REMOVE,
                node._id,
            ])

            return node

    def clear(self):
        with self._node.document.lock:
            if not self._nodes:
                return

            for node in list(self._nodes):
                node.parent = None
                self._nodes.remove(node)

            self._changes.append([
                monotonic_ns(),
                self._node._id,
                PATCH_TYPE.NODES,
                OPERATION.CLEAR,
            ])

    def __getitem__(self, index):
        with self._node.document.lock:
            return self._nodes[index]

    def __setitem__(self, index, node):
        node = self._check_node(node)

        with self._node.document.lock:
            self._prepare_node(node)
            self._nodes[index] = node

            self._changes.append([
                monotonic_ns(),
                self._node._id,
                PATCH_TYPE.NODES,
                OPERATION.SET,
                index,
                node._serialize(),
            ])

    def __bool__(self):
        with self._node.document.lock:
            return bool(self._nodes)

    def __len__(self):
        with self._node.document.lock:
            return self._nodes.__len__()

    def __iter__(self):
        with self._node.document.lock:
            return self._nodes.__iter__()

    # serialisation ###########################################################
    def _reset(self, value):
        if not isinstance(value, list):
            value = [value]

        with self._node.document.lock:
            self._nodes.clear()

            for node in value:
                node = self._check_node(node)
                self._prepare_node(node)
                self._nodes.append(node)

                self._changes.append([
                    monotonic_ns(),
                    self._node._id,
                    PATCH_TYPE.NODES,
                    OPERATION.RESET,
                    [i._serialize() for i in self._nodes]
                ])

    def _has_changes(self):
        return bool(self._changes)

    def _get_changes(self):
        return list(self._changes)

    def _clear_changes(self):
        for node in self._nodes:
            node._clear_changes()

        self._changes.clear()

    def _serialize(self):
        return [i._serialize() for i in self._nodes]

    # string representation ###################################################
    def __str__(self):
        with self._node.document.lock:
            return '\n'.join([str(i) for i in self._nodes])

    def __repr__(self):
        return '<NodeList({}))>'.format(repr(self._nodes))
