from Acquisition import aq_inner
from DateTime import DateTime

from zope.interface import noLongerProvides, alsoProvides
from zope.component import queryUtility, getMultiAdapter
from zope.interface import providedBy, implements

from Products.Five import BrowserView

from Products.statusmessages.interfaces import IStatusMessage
from plone.registry.interfaces import IRegistry

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode

from collective.collage.megamenu.interfaces import IMegamenuCapable, \
    IMegamenuEnabled, IMegamenuSettings
    
from collective.collage.megamenu.browser.interfaces import \
    IEnablerView, ICookedSettingsView
    
from collective.collage.megamenu import message_factory as _

from plone.memoize.instance import memoize

## Enabler/Disabler View
class EnablerView(BrowserView):
    implements(IEnablerView)

    def __init__(self, context, request):
        self.context = aq_inner(context)
        self.request = request
        self.globals_view = getMultiAdapter((self.context, self.request), name="plone")
        settings = getMultiAdapter((self.context, self.request), name="megamenu-settings")
        self.auto_hide = settings.auto_hide
        self.auto_show = settings.auto_show

    def enable(self):
        """ Applies IMegamenuEnabled marker interface to current folder
        """
        message = ""

        if not self.is_enabled():
            alsoProvides(self.context, IMegamenuEnabled)
            message = _(u"Folder can now be used as megamenu")
            if self.auto_hide:
                self._set_hidden(True)
            
        self._return_with_message(message)


    def disable(self):
        """ Removes IMegamenuEnabled marker interface from current folder
        """
        message = ""

        if self.is_enabled():
            noLongerProvides(self.context, IMegamenuEnabled)
            message = _(u"Folder can no longer be used as megamenu")
            if self.auto_show:
                self._set_hidden(False)


        self._return_with_message(message)
        
    @memoize
    def is_capable(self):
        """ Tells if this object is IMegamenuCapable
        """
        return IMegamenuCapable in providedBy(self.context)

    @memoize
    def is_enabled(self):
        """ Tells if this object is marked with IMegamenuEnabled
        """
        globals = self.globals_view
        if globals.isFolderOrFolderDefaultPage():
            folder = globals.getCurrentFolder()
            return IMegamenuEnabled in providedBy(folder)
        else:
            return False

    @memoize
    def is_disabled(self):
        """ Tells if this object isn't marked with IMegamenuEnabled
        """
        globals = self.globals_view
        if globals.isFolderOrFolderDefaultPage():
            folder = globals.getCurrentFolder()
            return not IMegamenuEnabled in providedBy(folder)
        else:
            return False

    def set_as_current(self):
        """ Provides a shortcut to set current object as current megamenu
            in control panel
        """
        request = self.request
        context = self.context
        title = safe_unicode(context.Title())
        message = _(u"Press 'Save' button to select '${title}' as Megamenu folder", mapping={'title': title})
        IStatusMessage(request).addStatusMessage(message, type="info")
        utool = getToolByName(context, 'portal_url')
        portal_url = utool.getPortalObject().absolute_url()
        uid = context.UID()
        url = '%s/@@megamenu-controlpanel?form.widgets.megamenu_folder:list=%s' % (portal_url, uid)
        return request.response.redirect(url)
        
    def _return_with_message(self, message):
        """ Redirects to previous URL (HTTP_REFERER) with a status message
        """
        request = self.request

        if message:
            self.context.reindexObject(idxs=['object_provides', ])
            IStatusMessage(request).addStatusMessage(message, type="info")

        return request.response.redirect(request.HTTP_REFERER)
        
    def _set_hidden(self, hide):
        """ Hides/Shows all contents by setting 'yesterday' as effective date
        """
        yesterday = DateTime()-1
        context = self.context
        catalog = getToolByName(context, 'portal_catalog')
        brains = catalog(path='/'.join(context.getPhysicalPath()))
        for brain in brains:
            try:
                object = brain.getObject()
                current = object.getExpirationDate()
                if hide:
                    # If has to hide, check if current expiration date (if any) is OK.
                    # If not, set expiration date
                    if current is None or current>yesterday:
                        object.setExpirationDate(yesterday)
                        object.reindexObject()
                else:
                    # If has to show, check if content has expiration date.
                    # If it has one and is previous than yesterday, remove it
                    if not current is None and current<yesterday:
                        object.setExpirationDate(None)
                        object.reindexObject()
            except:
                pass

## Configuration options View
class CookedSettingsView(BrowserView):
    implements(ICookedSettingsView)

    def __init__(self, context, request):
        self.context = aq_inner(context)
        self.request = request
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(IMegamenuSettings)
        self.enabled = settings.enabled and settings.megamenu_folder
        self.menufolder = None
        if self.enabled:
            self.menufolder = settings.megamenu_folder

        self.ajax = settings.deferred_rendering
        self.auto_hide = settings.auto_hide
        self.auto_show = settings.auto_show
        
    def resolve_folder(self, UID):
        catalog = getToolByName(self.context, 'portal_catalog')
        brain = catalog(UID=UID, show_inactive=True)
        menufolder = None
        if len(brain)>0:
            try:
                menufolder = brain[0].getObject()
            except:
                pass
        return menufolder
        

