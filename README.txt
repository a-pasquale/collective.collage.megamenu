Rough list of features
======================

Plone implementation of a mega drop-down menu based on 
http://www.sohtanaka.com/web-design/mega-drop-downs-w-css-jquery/.

Developed for Plone 3 and Plone 4.

Uses 
`collective.collage.nested <http://pypi.python.org/pypi/collective.collage.nested>`_ 
to support nested `Collage
<http://pypi.python.org/pypi/Products.Collage>`_ objects.

Adds some actions in portal_actions/object_buttons:

1. **Enable Megamenu**: adds ``IMegamenuEnabled`` interface to current folder.
#. **Current Megamenu**: selects current folder as current megamenu (the one
   that will be displayed in ``plone.portalheader`` viewlet manager).
#. **Disable Megamenu**: removes ``IMegamenuEnabled`` interface to current folder.
#. **Test Megamenu**: shows a preview of the current megamenu-enabled folder as if 
   it were *the* megamenu. 

Collage layout-views for ``ATCTContent``: ``menu`` and ``intro``.

Collage renderer-views for Collage, Rows and Columns used inside the above
layout-views. This is to provide cleaner HTML.

JavaScript and CSS resources to support megamenu. Special CSS for Plone classic 
theme (Plone 3 theme).

Native support for ATFolders (see ``atfolder.zcml``) and plone.app.folder 
(``ploneappfolder.zcm``) and can be extended for other custom folder implementations.

How-to create a megamenu
========================

1. Create a regular folder
#. Go to Actions | Enable Megamenu
#. Go to Actions | Current Megamenu to select the folder as the megamenu
   folder you want to display.
#. Create as many Link objects to internal or external URLs you want to
   include in megamenu as regular links (no drop-down). Description is
   rendered as ``title`` attribute.
#. Create as many Collage objects as items you want to show in your menu.
   Description is rendered as ``title`` attribute.
#. Add one related item in your Colage objects to provide a default link
   (for non-JavaScript enabled browsers).
#. Create as many rows and columns as you need in Collage and select the
   ``menu`` option in layout dropdown.
#. ``menu`` rows have several skins to display horizontal or vertical 
   separating lines between rows and columns.
#. Create as many objects as you need in the columns and select the ``menu`` 
   option in layout dropdown. 
#. ``menu`` items have three skins to display just the title (no link), 
   regular link or highlighted (strong) link.
#. Alternatively, you can select ``intro`` layout to provide more details:
   title, image and description.


Megamenu controlpanel
=====================

You can:

1. Enable / disable megamenu.
#. Select current megamenu folder (from all the folders providing 
   ``IMegamenuEnable`` interface).
#. Choose whether you want to include drop-down HTML markup in the page or
   load it via AJAX.
#. Automatically hide all folder contents (and folder itself) when 
   megamenu-enabling (by setting expiration date).
#. Automatically show all folder contents (and folder itself) when 
   megamenu-disabling (by removing expiration date).
   
Screenshots
===========

.. figure:: http://i.imgur.com/3r4g4l.jpg
    :figwidth: image
    :target: http://i.imgur.com/3r4g4.png
    
    Collage description is shown as ``title``. "Events" link highlighted 
    with ``selected`` CSS class. Second column with highlighted news item
    with ``intro`` layout.
    
.. figure:: http://i.imgur.com/eZXoBl.jpg
    :figwidth: image
    :target: http://i.imgur.com/eZXoB.png
    
    Three rows with one, two and three columns.
    
.. figure:: http://i.imgur.com/EdRWLl.jpg
    :figwidth: image
    :target: http://i.imgur.com/EdRWL.png
    
    Horizontal and vertical line separators
    
.. figure:: http://i.imgur.com/uBNQCl.jpg
    :figwidth: image
    :target: http://i.imgur.com/uBNQC.png
    
    Nested Collage: two columns, each of which with two rows.
    
.. figure:: http://i.imgur.com/BET2tl.jpg
    :figwidth: image
    :target: http://i.imgur.com/BET2t.png
    
    Megamenu with classic theme working in Plone 3.
