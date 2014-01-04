


var IndexController = (function() {

    /**
     * @param url {String}
     */
    var _addRandomToUrl = function(url) {
        if(url.indexOf('?') > 0) {
            var params = {};
            url.substr(url.indexOf('?')+1).split('&').each(function(x) {
                var parts = x.split('=');
                params[parts[0]] = parts[1];
            });

            params['_random'] = Math.random();

            return url.substr(0, url.indexOf('?')) + Object.toQueryString(params);
        }
        else {
            return url + '?_random=' + Math.random();
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
                img.src = _addRandomToUrl(img.src);
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

        dragHandler({
            element: el,
            onStart: function() {scrollStart = el.getScroll()},
            onDrag: function(ev) {el.scrollTo(scrollStart.x-ev.diff.x, scrollStart.y-ev.diff.y)},
            attach: true,
            name: "PanView" // for debugging purposes
        });
    };

    pub.initializeActionsHandlers = function() {
        $('imagesArea').getElement('.actions').addEvent('click', function(e) {
            var img = $('imagePreview').getElement('img');
            var imgUid = img.dataset['uid'];

            e.stop();
            //console.log('OMG CLICK', e);

            var actionType = e.target.dataset['actiontype'];

            if(actionType == 'zoom_in') {
                img.setStyles({
                    width: img.getSize().x*2,
                    height: img.getSize().y *2
                });
            }

            if(actionType == 'zoom_out') {
                img.setStyles({
                    width: img.getSize().x/2,
                    height: img.getSize().y/2
                });
            }

            if(actionType == 'rotate_left' || actionType == 'rotate_right') {
                var direction = (actionType == 'rotate_left' ? 'left' : 'right');

                new Request({
                    url: '/receipt_rotate/'+imgUid+'/' + direction,
                    method: 'GET',
                    onSuccess: function() {
                        IndexController.loadImage(imgUid);
                        _refreshThumbnail(imgUid);
                    }
                }).send();
            }
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


