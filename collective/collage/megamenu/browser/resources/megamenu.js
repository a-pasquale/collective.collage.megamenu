/* Copied and adapted from http://www.sohtanaka.com/web-design/mega-drop-downs-w-css-jquery/ */

jq(document).ready(function() {

    //Calculate width of all ul's
    (function(jq) {
        jQuery.fn.calcSubWidth = function() {
            // Should receive a .menu-row element
            var rowWidth = 0;
            //Calculate row
            jq(this).find(">ul").each(function() {
                rowWidth += jq(this).width();
            });
            return rowWidth;
        };
    }(jQuery));


    (function(jq) {
        jQuery.fn.resetWidth = function(nesting) {
            // Should receive a .sub element
            // Show the element (opacity = 0) to set widths properly
            if (!nesting) {
                this.css('opacity', 0).show();
            }
            // find all direct-child rows (there could be nested menues)
            var rows = this.find('>.menu-row');
            var biggestRow = 0;
            //Calculate each row
            rows.each(function() {
                // If there are nested menues, reset their widths before
                var me = jq(this);
                var nested = me.find('>ul>li.menu_view_nested-menu');
                nested.each(function() {
                    jq(this).resetWidth(true);
                });
                var rowWidth = me.calcSubWidth();
                //Find biggest row
                if (rowWidth > biggestRow) {
                    biggestRow = rowWidth;
                }
            });
            rows.each(function() {
                var columns = jq(this).find('>ul');
                var count = columns.length;
                columns.css('width', biggestRow / count);
            });

            biggestRow += 30; //Set width adding 15 + 15 px (left and right padding)
            this.css({
                'width': biggestRow
            });
            this.find(">.menu-row:last").css({
                'margin': '0'
            });
            if (!nesting) {
                this.hide();
            }
        };
    }(jQuery));

    String.prototype.startsWith = function(text) {
        return this.substring(0, text.length) === text;
    };

    function applySelected() {
        // Get all links and select their parent li-elements 
        // if href matches current URL beginning
        var url = document.location.href;
        jq('#portal-megamenu li.menu_view_menu a').each(function() {
            if (url.startsWith(this.href)) {
                jq(this).closest('li').addClass('selected');
            }
        });
    }

    function megaHoverOver() {
        var me = jq(this);
        // Check if there's another open menu (may be open because of a focused input or button)
        var currentlyActive = me.siblings('.active');
        if (currentlyActive.length > 0) {
            // If found an active menu, hide it
            hideMenu(currentlyActive);
            me.find('a').focus();
        }
        me.removeClass('hover').addClass('active').prev('li').addClass('nextActive');
        me.next('li').addClass('prevActive');
        var sub = me.find('.sub');
        if (sub.length > 0) {
            var shadow = sub.data('shadow');
            if (!shadow) {
                sub.after('<div class="subShadow" style="display: none;"></div>');
                shadow = sub.next('.subShadow');
                sub.data('shadow', shadow);
            }
            sub.stop().fadeTo(50, 1).show();
            shadow.stop().fadeTo(50, 0.6).show();

            var wWidth = jq(window).width();
            sub.css('left', 0);
            var sWidth = sub.width();
            var difWidth = wWidth - (sub.offset().left + sWidth + 19 + 20); //19px = scrollbar + 20px=padding
            var left = 0;
            if (difWidth < 0) {
                left = difWidth;
            }
            sub.css('left', left);
            shadow.css({
                left: left,
                width: sub.outerWidth(),
                height: sub.outerHeight()
            })
        }

    }

    function megaHoverOut() {
        var me = jq(this);
        var focusField = document.activeElement; // :focus in jQuery>=1.6
        if (focusField.nodeType == 1 && focusField.tagName.toLowerCase().match(/^(input|textarea|select|button)$/)) { // focusable form elements
            focusField = jq(focusField);
            if (focusField.closest('li.top-level.active').length > 0) {
                // if focused field is inside the menu, relay the hideMenu on click event
                jq(window).click(function(event) {
                    var target = jq(event.target);
                    // if clicked element is outside the active menu
                    var activeParent = target.closest('li.top-level.active');
                    if (activeParent.length === 0) {
                        // hide it
                        hideMenu(me);
                    }

                });
                return;
            }
        }

        hideMenu(me);
    }

    function hideMenu(me) {
        me = me || jq(this);
        me.removeClass('active').prev('li').removeClass('nextActive');
        me.next('li').removeClass('prevActive');
        var sub = me.find('.sub');
        if (sub.length > 0) {
            var shadow = sub.data('shadow');
            sub.stop().fadeTo(50, 0, function() {
                jq(this).hide();
            });
            if (shadow) {
                shadow.stop().fadeTo(50, 0, function() {
                    jq(this).hide();
                });
            }
        }
    }


    var config = {
        sensitivity: 2,
        // number = sensitivity threshold (must be 1 or higher)    
        interval: 200,
        // number = milliseconds for onMouseOver polling interval    
        over: megaHoverOver,
        // function = onMouseOver callback (REQUIRED)    
        timeout: 100,
        // number = milliseconds delay before onMouseOut    
        out: megaHoverOut // function = onMouseOut callback (REQUIRED)    
    };

    var megamenu = jq('#portal-megamenu');
    megamenu.find('li .sub').css({
        'opacity': '0'
    });
    // Bind over/out and click events of li.top-level
    megamenu.find('li.top-level').
    hover(function() {
        jq(this).addClass('hover');
    }, function() {
        jq(this).removeClass('hover');
    }).
    hoverIntent(config).
	// bind click event to show/hide drop-down
    click(function() {
		var me = jq(this);
		if (me.hasClass('active')) {
			hideMenu(me);
		} else {
			jq.proxy(megaHoverOver, me)();
		}
	}).
    // and Bind click event of their links-with-menues to prevent redirection
    find('a').click(function(event) {
        if (jq(this).closest('li').find('.sub').length > 0) {
            event.preventDefault();
        }
    });

    // Preload sub-menues, if there are deferred dropdowns
    var deferred = megamenu.find('a[rel=deferred]');
    if (deferred.length > 0) {
        megamenu.find('a[rel=deferred]').each(function() {
            jq(this).parent().load(this.href, function(response, status, request) {
                // Reset width
                jq(this).resetWidth();
                applySelected();
            });
        });
    } else {
        // If there aren't deferred dropdowns, just reset their widths
        megamenu.find('.sub').each(function() {
            jq(this).resetWidth();
            applySelected();
        });
    }

});