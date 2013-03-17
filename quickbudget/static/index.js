


var IndexController = (function() {

    var _loadImage = function(uid) {
        var preview = $('imagePreview');

        var img = new Element('img', {'data-uid': uid});

        img.addEvent('load', function() {
            var availSize = preview.getSize();
            var imgSize = img.getDimensions();

            var ratio = availSize.x / imgSize.width;

            img.setStyles({
                width: imgSize.width * ratio,
                height: imgSize.height * ratio
            });



            preview.grab(img);

            img.setStyle('opacity', 0);
            img.setStyle('display', null);

            //img.setStyle('display', null);
            //new Fx.Morph(img, {styles: []}).reveal();
            img.fade('in');
        });

        img.setStyle('display', 'none');
        img.src = '/receipt_thumb/'+uid+'/full';
        document.body.grab(img);
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

    pub.resizeWorkingArea = function() {
        var availableHeight = $(window).getSize().y;
        //var scrollSize = getScrollBarWidth();

        var mainArea = $('connectArea');

        availableHeight -= mainArea.getPosition().y;

        $('receiptListContainer').setStyle('height', availableHeight);

        var scrollArea = $('imageListContainer').getElement('.scrollarea');

        scrollArea.setStyle('width', $('imagesArea').getSize().x);

        //console.log('OMG', scrollArea.getSize().y, '::', scrollSize);
        $('imageListContainer').setStyle('height', scrollArea.getSize().y);

        var previewSize = availableHeight;
        previewSize -= $('imageListContainer').getSize().y;
        previewSize -= $('imagesArea').getElement('.actions').getSize().y;

        $('imagePreview').setStyle('height', previewSize);
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

                        $('imageList').getElements('img').each(function(img) {
                            if(img.dataset['imguid'] == imgUid) {
                                img.src = img.src;
                            }
                        });
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
            }
        });
    };


    return pub;

})();


