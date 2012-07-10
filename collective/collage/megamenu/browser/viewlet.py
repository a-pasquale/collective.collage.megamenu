from Acquisition import aq_inner
from plone.app.layout.viewlets import common
from zope.component import getMultiAdapter
from zope.interface import providedBy
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.collage.megamenu.interfaces import IMegamenuEnabled

from zope.interface import noLongerProvides, alsoProvides, implements
from Products.CMFCore.utils import getToolByName

from Products.Collage.interfaces import ICollageEditLayer
from plone.memoize.instance import memoize


class MegamenuViewlet(common.ViewletBase):
    """ Viewlet to display megamenu
    """
    
    def update(self):
        context = aq_inner(self.context)
        request = self.request
        self.settings = getMultiAdapter((context, request), name="megamenu-settings")
        # If testing a megamenu, use the requested folder instead of the one
        # specified in controlpanel
        self.test_folder_uid = request.form.get('megamenu-test')
        if self.test_folder_uid:
            self.testing = self.settings.menufolder != self.test_folder_uid
        else:
            self.testing = False
                     

    @memoize
    def menufolder(self):
        context = self.context
        request = self.request
        if self.test_folder_uid:
            folder = self.settings.resolve_folder(self.test_folder_uid)
        else:
            folder = self.settings.resolve_folder(self.settings.menufolder)
            
        if not IMegamenuEnabled in providedBy(folder):
            folder = None
        return folder
        
    def folder_title(self):
        folder = self.menufolder()
        return folder.Title()
    
    def folder_url(self):
        folder = self.menufolder()
        return folder.absolute_url()
        
    index = ViewPageTemplateFile('templates/viewlet.pt')
