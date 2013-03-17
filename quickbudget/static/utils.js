

function getScrollBarWidth () {
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
    if (w1 == w2) w2 = outer.clientWidth;

    document.body.removeChild (outer);

    return (w1 - w2);
}


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
var dragHandler = function(params) {
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
        if (params.onBeforeStart
            && !params.onBeforeStart({event: e, element: params.element})) {
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