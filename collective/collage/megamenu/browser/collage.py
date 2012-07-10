from Acquisition import aq_inner

from zope.interface import Interface
from zope.component import getMultiAdapter
from zope.interface import providedBy

from Products.Collage.browser.views import BaseView, RowView
from Products.Collage.interfaces import ICollageEditLayer
from Products.ATContentTypes.interface import IATLink

from collective.collage.megamenu import message_factory as _
from plone.memoize.instance import memoize


## Menu item

class IMenuLayoutSkin(Interface):
    """Interface for skinable views."""
    pass

class BasicMenuLayout(BaseView):
    skinInterfaces = (IMenuLayoutSkin, )
    
    title = _(u"Menu")
    
    @memoize
    def object(self):
        return aq_inner(self.context)
        
    def url(self):
        object = self.object()
        # If it's a link
        if IATLink in providedBy(object):
            remoteUrl = object.getRemoteUrl()
            # If it's a local link
            if remoteUrl[0] == '/':
                # Get portal object and re-create link
                context = aq_inner(self.context)
                request = self.request
                portal_state = getMultiAdapter((context, request), name="plone_portal_state")
                return '%s%s' % (portal_state.portal_url(), remoteUrl)
            else:
                return remoteUrl
        else:
            # Otherwise, return object's url
            return object.absolute_url()
    
# Skins
class TitleSkin(object):
    title = _(u"Title")

class LinkSkin(object):
    title = _(u"Link")

class HighlightedLinkSkin(object):
    title = _(u"Highlight")

### MenuRow

class IMenuRowLayoutSkin(Interface):
    """Interface for skinable views."""
    pass

class MenuRowLayout(RowView):
    """ Special RowView """
    
    skinInterfaces = (IMenuRowLayoutSkin, )
    
    title = _(u"Menu")

    def inComposeView(self):
        return ICollageEditLayer in providedBy(self.request)
 
 
 # Skins
class NoLinesSkin(object):
    title = _(u"No line")
    
class HLinesSkin(object):
    title = _(u"Bottom line")

class VLinesSkin(object):
    title = _(u"Vertical lines")
    
class HVLinesSkin(object):
    title = _(u"Both lines")

