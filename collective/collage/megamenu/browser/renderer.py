from Acquisition import aq_inner

from zope.interface import noLongerProvides, alsoProvides, implements
from zope.component import getMultiAdapter
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from Products.Collage.interfaces import ICollageEditLayer

from collective.collage.megamenu.browser.interfaces import IMenuRenderer

### Menu Renderer view

class MenuRenderer(BrowserView):
    implements(IMenuRenderer)

    def getItems(self):
        context = self.context
        request = self.request
        portal_state = getMultiAdapter((context, request), name="plone_portal_state")
        portal_url = portal_state.portal_url()
        settings = getMultiAdapter((context, request), name="megamenu-settings")
        ajax = settings.ajax
        # TODO: Restrict items?
        # Taken from Products/CMFPlone/skins/plone_scripts/getFolderContents.py to bypass show_inactive filter
        catalog = getToolByName(context, 'portal_catalog')
        query = {}
        query['sort_on'] = 'getObjPositionInParent'
        path = {}
        path['query'] = '/'.join(context.getPhysicalPath())
        path['depth'] = 1
        query['path'] = path
        contents = catalog.queryCatalog(query, show_all=1, show_inactive=True, )
        #contents = self.context.getFolderContents(contentFilter={'show_inactive': True})
        
        # Before getting items (actually, before rendering them), remove ICollageEditLayer from request
        composing = ICollageEditLayer.providedBy(request)
        if composing:
            noLongerProvides(request, ICollageEditLayer)
            
        current_url = request.get('ACTUAL_URL') + '/'
        items = []
        for content in contents:
            item = {}
            item['id'] = content.getId
            item['object'] = content
            is_collage = content.meta_type == 'Collage'
            if is_collage:
                collage = content.getObject()
                
            item['with_menu'] = is_collage
            item['title'] = content.Title or ''
            item['description'] = content.Description or ''
            if content.meta_type == 'ATLink':
                # For ATLinks, get the link
                remoteUrl = content.getRemoteUrl
                if remoteUrl[0] == '/':
                    item['url'] = '%s%s' % (portal_url, remoteUrl)
                else:
                    item['url'] = remoteUrl
            else:
                # For other contents, get its url
                item['url'] = content.getURL()
                if is_collage:
                    # Bug if it's a Collage, try to get its first related item
                    related = collage.getRelatedItems()
                    if len(related)>0:
                        item['url'] = related[0].absolute_url();


            # Should item be rendererd as 'selected'?
            # 1. item.url==portal_url and current_url==item.url
            # 2. item.url!=portal_url and current_url.startswith(item.url)
            if (item['url']==portal_url+'/' and current_url==item['url']) or \
               (item['url']!=portal_url+'/' and current_url.startswith(item['url'])):
                item['selected_class'] = 'selected'
            else:
                item['selected_class'] = ''
                
            if is_collage:
                item['class'] = 'menu-dropdown'
                if not ajax:
                    item['dropdown'] = collage.restrictedTraverse('@@menu-renderer')()
                    item['deferred'] = ''
                else:
                    item['dropdown'] = ''
                    item['deferred'] = '%s%s' % (content.getURL(), '/@@menu-renderer')
            else:
                item['class'] = ''
                item['dropdown'] = None
                item['deferred'] = ''
                
            items.append(item)

        if composing:
            alsoProvides(request, ICollageEditLayer)
            
        return items
