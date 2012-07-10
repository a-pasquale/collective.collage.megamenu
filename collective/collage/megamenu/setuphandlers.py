# -*- coding: utf-8 -*-
"""Custom import steps"""

from Products.CMFCore.utils import getToolByName

# Check for Plone versions
try:
    from plone.app.upgrade import v40
    HAS_PLONE40 = True
except ImportError:
    HAS_PLONE40 = False

def is_not_megamenu_default_profile(context):
    return context.readDataFile("collective_collage_megamenu_default.txt") is None


def setup_various(context):
    """Various setup steps"""

    if is_not_megamenu_default_profile(context):
        return

    portal = context.getSite()
    setup = getToolByName(portal, 'portal_setup')
    if not HAS_PLONE40:
        setup.runAllImportStepsFromProfile('profile-collective.collage.megamenu:plone3')
