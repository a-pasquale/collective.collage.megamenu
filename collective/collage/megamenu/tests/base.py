"""Test setup for integration and functional tests.

When we import PloneTestCase and then call setupPloneSite(), all of
Plone's products are loaded, and a Plone site will be created. This
happens at module level, which makes it faster to run each test, but
slows down test runner startup.
"""

from Products.Five import zcml
from Products.Five import fiveconfigure

from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

from Products.CMFCore.utils import getToolByName

from Products.Collage.interfaces import IDynamicViewManager
from zope.component import getUtility
from plone.app.viewletmanager.interfaces import IViewletSettingsStorage


import os
from App import Common

# When ZopeTestCase configures Zope, it will *not* auto-load products
# in Products/. Instead, we have to use a statement such as:
#   ztc.installProduct('SimpleAttachment')
# This does *not* apply to products in eggs and Python packages (i.e.
# not in the Products.*) namespace. For that, see below.
# All of Plone's products are already set up by PloneTestCase.

@onsetup
def setup_product():
    """Set up the package and its dependencies.

    The @onsetup decorator causes the execution of this body to be
    deferred until the setup of the Plone site testing layer. We could
    have created our own layer, but this is the easiest way for Plone
    integration tests.
    """

    # Load the ZCML configuration for the example.tests package.
    # This can of course use <include /> to include other packages.

    fiveconfigure.debug_mode = True
    import collective.collage.megamenu
    zcml.load_config('configure.zcml', collective.collage.megamenu)
    fiveconfigure.debug_mode = False

    # We need to tell the testing framework that these products
    # should be available. This can't happen until after we have loaded
    # the ZCML. Thus, we do it here. Note the use of installPackage()
    # instead of installProduct().
    # This is *only* necessary for packages outside the Products.*
    # namespace which are also declared as Zope 2 products, using
    # <five:registerPackage /> in ZCML.

    # We may also need to load dependencies, e.g.:
    #   ztc.installPackage('borg.localrole')

    ztc.installPackage('collective.collage.megamenu')

# The order here is important: We first call the (deferred) function
# which installs the products we need for this product. Then, we let
# PloneTestCase set up this product on installation.

setup_product()
ptc.setupPloneSite(products=['collective.collage.megamenu'])

class TestCase(ptc.PloneTestCase):
    """We use this base class for all the tests in this package. If
    necessary, we can put common utility or setup code in here. This
    applies to unit test cases.
    """

from OFS.interfaces import IFolder
class ISpecialFolder(IFolder):
    pass

class FunctionalTestCase(ptc.FunctionalTestCase):
    """We use this class for functional integration tests that use
    doctest syntax. Again, we can put basic common utility or setup
    code in here.
    """

    def afterSetUp(self):
        roles = ('Member', 'Contributor')
        self.portal.portal_membership.addMember('contributor',
                                                'secret',
                                                roles, [])
                                                
class FunctionalTestCaseWithContent(FunctionalTestCase):

    class Session(dict):
        def set(self, key, value):
            self[key] = value

    def _setup(self):
        FunctionalTestCase._setup(self)
        self.app.REQUEST['SESSION'] = self.Session()


    def afterSetUp(self):
        super(FunctionalTestCase, self).afterSetUp()
        self.loginAsPortalOwner()
        wtool = getToolByName(self.portal, 'portal_workflow')
        
        # Menu Folder
        id = self.portal.invokeFactory('Folder', 'menu')
        ob = getattr(self.portal, id)
        ob.setTitle('Menu folder')
        wtool.doActionFor(ob, 'publish')
        menu = ob
        self.menu = menu
        
        # First item in menu: an internal link to home
        id = menu.invokeFactory('Link', 'home-link')
        ob = getattr(menu, id)
        ob.setTitle('Home')
        ob.setRemoteUrl('/')
        wtool.doActionFor(ob, 'publish')
        elink = ob

        # Get image file
        pkg_home = Common.package_home({'__name__': 'collective.collage.megamenu'})
        samplesdir = os.path.join(pkg_home, 'tests', 'samples')
        image_file = file(os.path.join(samplesdir, 'test_image.png')).read()

        # Image
        id = self.portal.invokeFactory('Image', 'image')
        ob = getattr(self.portal, id)
        ob.setTitle('Test image')
        ob.setDescription('Dummy description for image')
        ob.setImage(image_file)
        # Image is automatically published
        image = ob
        
        # News item with image
        id = self.portal.invokeFactory('News Item', 'news-item')
        ob = getattr(self.portal, id)
        ob.setTitle('Test news item')
        ob.setDescription('Dummy description for news item')
        ob.setImage(image_file)
        wtool.doActionFor(ob, 'publish')
        ni = ob
        
        # Page (Document)
        id = self.portal.invokeFactory('Document', 'doc')
        ob = getattr(self.portal, id)
        ob.setTitle('Test document')
        ob.setDescription('Dummy description for document')
        wtool.doActionFor(ob, 'publish')
        doc = ob
        
        # Folder 1
        id = self.portal.invokeFactory('Folder', 'folder-1')
        ob = getattr(self.portal, id)
        ob.setTitle('Test folder #1')
        ob.setDescription('Dummy description for folder 1')
        wtool.doActionFor(ob, 'publish')
        folder1 = ob

        # Folder 2
        id = self.portal.invokeFactory('Folder', 'folder-2')
        ob = getattr(self.portal, id)
        ob.setTitle('Test folder #2')
        ob.setDescription('Dummy description for folder 2')
        wtool.doActionFor(ob, 'publish')
        folder2 = ob
        
        # External link
        id = self.portal.invokeFactory('Link', 'external-link')
        ob = getattr(self.portal, id)
        ob.setTitle('External link')
        ob.setDescription('External link to plone.org')
        ob.setRemoteUrl('http://plone.org/')
        wtool.doActionFor(ob, 'publish')
        elink = ob
        
        # Internal link
        id = self.portal.invokeFactory('Link', 'internal-link')
        ob = getattr(self.portal, id)
        ob.setTitle('Internal link')
        ob.setDescription('Internal link to no-where')
        ob.setRemoteUrl('/no-where')
        wtool.doActionFor(ob, 'publish')
        ilink = ob

        # Pre-build a Collage with aliases for each of the just created objects
        # and set the layout
        id = menu.invokeFactory('Collage', 'collage')
        collage = getattr(menu, id)
        collage.setTitle('Collage')
        wtool.doActionFor(collage, 'publish')
        self.collage = collage

        # Row & first column
        id = collage.invokeFactory('CollageRow', '1')
        row = getattr(collage, id)
        manager = IDynamicViewManager(row)
        manager.setLayout('menu')
        id = row.invokeFactory('CollageColumn', '1')
        column = getattr(row, id)
        manager = IDynamicViewManager(column)
        manager.setLayout('menu')
        
        # Alias for image
        id = column.invokeFactory('CollageAlias', 'alias-1')
        alias1 = getattr(column, id)
        alias1.set_target(image.UID())
        manager = IDynamicViewManager(alias1)
        manager.setLayout('menu')
        manager.setSkin('collage-megamenu-highlight')

        # Alias for document
        id = column.invokeFactory('CollageAlias', 'alias-2')
        alias2 = getattr(column, id)
        alias2.set_target(doc.UID())
        manager = IDynamicViewManager(alias2)
        manager.setLayout('menu')
        manager.setSkin('collage-megamenu-title')
        
        # Alias folder 1
        id = column.invokeFactory('CollageAlias', 'alias-3')
        alias3 = getattr(column, id)
        alias3.set_target(folder1.UID())
        manager = IDynamicViewManager(alias3)
        manager.setLayout('menu')

        # Alias for folder 2
        id = column.invokeFactory('CollageAlias', 'alias-4')
        alias4 = getattr(column, id)
        alias4.set_target(folder2.UID())
        manager = IDynamicViewManager(alias4)
        manager.setLayout('menu')
        
        # Alias for external link
        id = column.invokeFactory('CollageAlias', 'alias-5')
        alias5 = getattr(column, id)
        alias5.set_target(elink.UID())
        manager = IDynamicViewManager(alias5)
        manager.setLayout('menu')

        # Alias for internal link
        id = column.invokeFactory('CollageAlias', 'alias-6')
        alias6 = getattr(column, id)
        alias6.set_target(ilink.UID())
        manager = IDynamicViewManager(alias6)
        manager.setLayout('menu') 
        
        # Second column to add an intro layout
        id = row.invokeFactory('CollageColumn', '2')
        column = getattr(row, id)
        manager = IDynamicViewManager(column)
        manager.setLayout('menu')
        # Alias for news item intro
        id = column.invokeFactory('CollageAlias', 'alias-7')
        alias7 = getattr(column, id)
        alias7.set_target(ni.UID())
        manager = IDynamicViewManager(alias7)
        manager.setLayout('intro')
        
        # Alternate menu with just one link
        id = self.portal.invokeFactory('Folder', 'other-menu')
        ob = getattr(self.portal, id)
        ob.setTitle('Alternative menu')
        wtool.doActionFor(ob, 'publish')
        self.other_menu = ob
        
        # Another internal link
        id = self.other_menu.invokeFactory('Link', 'another-link')
        ob = getattr(self.other_menu, id)
        ob.setTitle('Another link')
        ob.setDescription('Internal link to somewhere')
        ob.setRemoteUrl('/somewhere')
        wtool.doActionFor(ob, 'publish')
