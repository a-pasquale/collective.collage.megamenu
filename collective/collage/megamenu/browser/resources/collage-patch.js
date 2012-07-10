/* Override collage.js triggerMove function to get items variable from
   current Collage object instead of from the whole DOM
*/
triggerMove = function(event, direction) {
    var $ = jq;
    
    $ = event.data.jquery;
    event.preventDefault();

    var link = $(this);
    link.blur();
    
    var className = event.data.className;
    
    var row = link.parents('.collage-row').eq(0);
    var column = link.parents('.collage-column').eq(0);
    var item = link.parents('.collage-item').eq(0);

    var destination = null;
    var origin = null;
    var items = null;

    if (item.length) {
		items = item.parents('#collage').find('.collage-item', column);
		origin = $(item);
    } else if (column.length) {
		items = column.parents('#collage').find('.collage-column', row);
		origin = $(column);
    } else {
		items = row.parents('#collage').find('.collage-row');
		origin = $(row);
    }

    var index = items.index(origin.get(0));
    if (!(index+direction >= 0 && index+direction < items.length)) return false;
    
    destination = $(items[index+direction]);
    swap(origin, destination);

    doSimpleQuery(link.attr('href'));    
}