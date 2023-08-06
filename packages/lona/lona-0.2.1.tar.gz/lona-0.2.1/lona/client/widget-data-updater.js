Lona.LonaWidgetDataUpdater = function(lona_context, lona_window) {
    this.lona_context = lona_context;
    this.lona_window = lona_window;

    this._apply_patch = function(patch) {
        var node_id = patch[0];
        var patch_type = patch[1];
        var key_path = patch[2];
        var operation = patch[3];
        var data = patch.splice(4);

        // key path
        var parent_data = undefined;
        var widget_data = this.lona_window._widget_data[node_id];

        key_path.forEach(function(key) {
            parent_data = widget_data;
            widget_data = widget_data[key];
        });

        // SET
        if(operation == Lona.symbols.OPERATION.SET) {
            widget_data[data[0]] = data[1];

        // RESET
        } else if(operation == Lona.symbols.OPERATION.RESET) {
            if(parent_data === undefined) {
                this.lona_window._widget_data[node_id] = data[0];

            } else {
                parent_data = data[0];

            };

        // CLEAR
        } else if(operation == Lona.symbols.OPERATION.CLEAR) {
            if(widget_data instanceof Array) {
                var new_data = [];

            } else if(widget_data instanceof Object) {
                var new_data = {};

            };

            if(parent_data === undefined) {
                this.lona_window._widget_data[node_id] = new_data;

            } else {
                parent_data[key_path[key_path.length-1]] = new_data;

            };

        // INSERT
        } else if(operation == Lona.symbols.OPERATION.INSERT) {
            widget_data.splice(data[0], 0, data[1]);

        // REMOVE
        } else if(operation == Lona.symbols.OPERATION.REMOVE) {
            if(widget_data instanceof Array) {
                widget_data.splice(data[0], 1);

            } else if(data instanceof Object) {
                delete widget_data[data[0]];

            };
        };

       this.lona_window._widgets_to_update_data.splice(0, 0, node_id);
    };
};
