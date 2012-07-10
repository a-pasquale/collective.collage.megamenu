from zope.interface import providedBy
from collective.collage.megamenu.interfaces import IMegamenuEnabled
from Products.CMFCore.utils import getToolByName

def getIcon(self, relative_to_portal=0):
    utool = getToolByName(self, 'portal_url')
    portal_url = utool()
    icon = '++resource++collective.collage.megamenu/megamenu.gif'
    
    if IMegamenuEnabled in providedBy(self):
        if relative_to_portal==1:
            return icon
        else:
            return '%s/%s' % (portal_url, icon)
    else:
        return self._old_getIcon(relative_to_portal)
