
//noinspection JSUnusedGlobalSymbols,JSHint
function getScrollBarWidth () {
    "use strict";

    var inner = document.createElement('p');
    inner.style.width = "100%";
    inner.style.height = "200px";

    var outer = document.createElement('div');
    outer.style.position = "absolute";
    outer.style.top = "0px";
    outer.style.left = "0px";
    outer.style.visibility = "hidden";
    outer.style.width = "200px";
    outer.style.height = "150px";
    outer.style.overflow = "hidden";
    outer.appendChild (inner);

    document.body.appendChild (outer);
    var w1 = inner.offsetWidth;
    outer.style.overflow = 'scroll';
    var w2 = inner.offsetWidth;
    if (w1 === w2) {
        w2 = outer.clientWidth;
    }

    document.body.removeChild (outer);

    return (w1 - w2);
}

Utils = (function() {
    "use strict";

    var pub = {};

    pub.addRandomToUrl = function(url) {
        if(url.indexOf('?') > 0) {
            var params = {};
            url.substr(url.indexOf('?')+1).split('&').each(function(x) {
                var parts = x.split('=');
                params[parts[0]] = parts[1];
            });

            params['_random'] = Math.random();

            return url.substr(0, url.indexOf('?')+1) + Object.toQueryString(params);
        }
        else {
            return url + '?_random=' + Math.random();
        }
    };

    /**
     * @param {Object} params initalization parameters.
     * @config {Element} element DOM Element to which drag handler (mouse events listeners) will be attached.
     * @config {Boolean} [attach] if handler shoud be automatically activated.
     * @config {Function} [onBeforeStart] callable invoked when user presses mouse button, but before actually starting drag.
     * Receives event object. When onBeforeStart returns false, dragging doesn't happen.
     * @config {Function} [onStart] callable invoked when user presses mouse button.
     * Receives object {position: {x: Number, y: Number}} when called.
     * @config {Function} [onDrag] callable invoked at each mouse move when dragging.
     * Receives object {element: Element, diff: {x: Number, y: Number}} when called.
     * @config {Function} [onEnd] callable invoked when user releases mouse button. No parameters passed.
     * @config {String} [name] for debug purposes
     *
     *
     */
    pub.dragHandler = function(params) {
        var dragStart;

        var mouseMove = function(e) {
            e.stop();

            var diff = {
                x: e.page.x - dragStart.x,
                y: e.page.y - dragStart.y
            };

            params.onDrag({
                element: params.element,
                diff: diff
            });
        };

        var startDragging = function(e) {
            e.stop();
            dragStart = e.page;

            // XXX passing event breaks encapsulation a little bit...
            // XXX better name than onBeforeStart...
            if (params.onBeforeStart && !params.onBeforeStart({event: e, element: params.element})) {
                return;
            }

            document.addEvent('mousemove', mouseMove);
            document.addEvent('mouseup', stopDragging);

            if(params.onStart) {
                params.onStart({position:dragStart});
            }
        };

        var stopDragging = function(e) {
            e.stop();

            document.removeEvent('mousemove', mouseMove);
            document.removeEvent('mouseup', stopDragging);

            if(params.onEnd) {
                params.onEnd();
            }

        };

        var pub =  {
            attach: function() {
                params.element.addEvent('mousedown', startDragging);
            },
            detach: function() {
                params.element.removeEvent('mousedown', startDragging);
            },
            setAttached: function(shoudAttach) {
                if(shoudAttach) {
                    pub.attach();
                }
                else {
                    pub.detach();
                }
            }
        };

        if(params.attach) {
            pub.attach();
        }

        return pub;
    };

    return pub;
})();

Ui = (function(){
    "use strict";

    var pub = {};

    pub.openModalDialog = function(dialog) {
        var content = new Element('div', {'class':'mask_content'});
        document.body.grab(content);

        var maskTarget = document.body;

        var mask = new Mask(maskTarget, {
            onShow: function() {
                content.grab($(dialog));

                content.position({
                    relativeTo: $(this).getParent(),
                    position: 'center'
                });
            },
            onHide: function() {
                content.empty();
                content.destroy();
            }
        });

        dialog.addEvent('modalclose', function() {
            mask.hide();
        });

        mask.show();
    };

    /**
     *
     * @param {Element|String} message
     * @param {Object} [options]
     * @config {Integer} [width]
     * @config {Function} [onDone]
     * @config {String} [okText]
     */
    pub.messageDialog = function(message, options) {
        options = options || {};
        var dialog = new Element('div', {'class':'modalDialog'});
        var content = message;

        if(! (content instanceof Element)) {
            content = new Element('div', {html:message});
        }
        if(options.width) {
            dialog.setStyle('width', options.width+'px');
        }

        var onDone = function(e) {
            e.stop();
            if(options.onDone) {
                options.onDone();
            }
            dialog.fireEvent('modalclose');
        };

        var btnOk = new Element('button', {text: options.okText||'Ok'});

        btnOk.addEvent('click', onDone);

        dialog.grab(content);
        dialog.grab(new Element('div', {'class':'buttons'}).adopt([btnOk]));

        pub.openModalDialog(dialog);
    };

    return pub;
})();