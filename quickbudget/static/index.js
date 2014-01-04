


var IndexController = (function() {

    var actionHandlers = {
        zoom_in: function() {
            var img = $('imagePreview').getElement('img');
            img.setStyles({
                width: img.getSize().x*2,
                height: img.getSize().y *2
            });
        },
        zoom_out: function() {
            var img = $('imagePreview').getElement('img');
            img.setStyles({
                width: img.getSize().x/2,
                height: img.getSize().y/2
            });
        },
        rotate_left: function() {
            var img = $('imagePreview').getElement('img');
            var imgUid = img.dataset['uid'];

            var direction = 'left';

            new Request({
                url: '/receipt_rotate/'+imgUid+'/' + direction,
                method: 'GET',
                onSuccess: function() {
                    IndexController.loadImage(imgUid);
                    _refreshThumbnail(imgUid);
                }
            }).send();
        },
        rotate_right: function() {
            var img = $('imagePreview').getElement('img');
            var imgUid = img.dataset['uid'];

            var direction = 'right';

            new Request({
                url: '/receipt_rotate/'+imgUid+'/' + direction,
                method: 'GET',
                onSuccess: function() {
                    IndexController.loadImage(imgUid);
                    _refreshThumbnail(imgUid);
                }
            }).send();
        }
    };

    var _loadImage = function(uid) {
        var preview = $('imagePreview');

        var imgSrc = '/receipt_thumb/'+uid+'/full?_random=' + Math.random();

        Asset.image(imgSrc, {
            onLoad: function() {
                var img = new Element('img', {'data-uid': uid, src: imgSrc});

                preview.grab(img);
                img.setStyle('opacity', 0);

                var availSize = preview.getSize();
                var imgSize = img.getDimensions();

                var ratio = availSize.x / imgSize.width;

                img.setStyles({
                    width: imgSize.width * ratio,
                    height: imgSize.height * ratio
                });



                img.fade('in');
            }
        });
    };

    var _refreshThumbnail = function(imgUid) {
        $('imageList').getElements('img').each(function(img) {
            if(img.dataset['imguid'] == imgUid) {
                img.src = Utils.addRandomToUrl(img.src);
            }
        });
    };

    var pub = {};

    pub.loadImage = function(uid) {
        var oldImg = $('imagePreview').getElement('img');

        if(oldImg) {
            oldImg.fade('out').get('tween').chain(function() {
                oldImg.destroy();
                _loadImage(uid);
            });
        }
        else {
            _loadImage(uid);
        }
    };

    pub.initializePanView = function() {
        var el = $('imagePreview');
        var scrollStart = null;

        Utils.dragHandler({
            element: el,
            onStart: function() {scrollStart = el.getScroll()},
            onDrag: function(ev) {el.scrollTo(scrollStart.x-ev.diff.x, scrollStart.y-ev.diff.y)},
            attach: true,
            name: "PanView" // for debugging purposes
        });
    };

    pub.initializeActionsHandlers = function() {
        $('imagesArea').getElement('.actions').addEvent('click', function(e) {
            e.stop();

            var actionType = e.target.dataset['actiontype'];

            actionHandlers[actionType]();
        });
    };

    pub.initializeThumbnailSwitcher = function() {
        $('imageList').addEvent('click', function(e) {
            e.stop();
            var imgUid = e.target.dataset['imguid'];

            if(imgUid) {
                IndexController.loadImage(imgUid);

                var selected = e.target.getParent('ul').getElement('.selected');
                if(selected) {
                    selected.removeClass('selected');
                }

                e.target.getParent('li').addClass('selected');
            }
        });


    };

    pub.initializeHorizontalScroll = function() {
        var scrollable = $('imageList');

        scrollable.addEvent('mousewheel', function(e) {
            var isDown;

            if(e.event.wheelDelta) {
                isDown = (e.event.wheelDelta < 0);
            }
            else if(e.event.detail) {
                isDown = (e.event.detail > 0);
            }

            if(typeof isDown !== 'undefined') {
                var s = scrollable.getScroll();

                if(isDown) {
                    scrollable.scrollTo(s.x + 50, s.y);
                }
                else {
                    scrollable.scrollTo(s.x - 50, s.y);
                }
            }

        })
    };

    pub.loadFirstThumbnail= function() {
        var img = $('imageList').getElement('img');

        pub.loadImage(img.dataset['imguid']);
    };


    return pub;

})();


