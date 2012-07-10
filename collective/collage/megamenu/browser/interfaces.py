from zope.interface import Interface, Attribute
                            
class ICookedSettingsView(Interface):
    """ A browser view with some processing of control panel settings
    """
    menufolder = Attribute("""UID of fodler that is used to display megamenu""")
    enabled = Attribute("""Should display megamenu? Folder is megamenu-enabled?""")
    ajax = Attribute("""Load drop-down submenues via AJAX""")
    auto_hide = Attribute("""Auto-hide contents when enabling megamenu""")
    auto_show = Attribute("""Auto-show contents when disabling megamenu""")
    
    def resolve_folder(UID):
        """ Given a UID, get the folder via catalog
        """
        
class IEnablerView(Interface):
    """ A generic class with several methods that are used in
        several browser views
    """
    
    def enable():
        """ Enable a folder as megamenu
        """
        
    def disable():
        """ Disable a folder as megamenu
        """
        
    def is_capable():
        """ Is this object a megamenu-capable object (i.e. is a folder)?
        """
        
    def is_enabled():
        """ Is this object a megamenu-enabled object?
        """
        
    def is_disabled():
        """ Is this object a megamenu-disabled object?
        """
        
    def set_as_current():
        """ Set current object as current megamenu
        """
        
class IMenuRenderer(Interface):
    """ A browser view to get all "menuable" elements in a folder
    """
    
    def getItems():
        """ Return all items in the folder
        """
