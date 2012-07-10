from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.app.component.hooks import getSite
from Products.CMFCore.utils import getToolByName
from collective.collage.megamenu.interfaces import IMegamenuEnabled

def megamenues_vocabulary(context):
    """
    A list of all megamenu enabled objects in site
    
    @param context: Assume Plone site.
    
    @return: SimpleVocabulary containing (menu UID, menu Title)
    """
    try:
        import plone.registry.record
        import plone.registry.recordsproxy
        if isinstance(context, plone.registry.record.Record) or \
        isinstance(context, plone.registry.recordsproxy.RecordsProxy):
            context = getSite()
    except ImportError:
        pass
           
    catalog = getToolByName(context, 'portal_catalog', None)
    if catalog is None:
        return SimpleVocabulary([])

    brains = catalog(object_provides=IMegamenuEnabled.__identifier__)

    terms = []

    for menu in brains:
        terms.append(SimpleTerm(value=menu.UID, token=menu.UID, title=menu.Title))

    return SimpleVocabulary(terms)
