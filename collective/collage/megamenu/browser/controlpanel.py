from plone.app.registry.browser import controlpanel
from plone.z3cform import layout
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form.browser.radio import RadioFieldWidget

from collective.collage.megamenu.interfaces import IMegamenuSettings
from collective.collage.megamenu import message_factory as _


class MegamenuSettingsEditForm(controlpanel.RegistryEditForm):
    """ A configlet form for IMegamenuSettings
        based on plone.app.registry.controlpanel
    """
    schema = IMegamenuSettings
    label = _(u"Megamenu settings")

    
    def updateFields(self):
        """ Set form widgets
        """
        super(MegamenuSettingsEditForm, self).updateFields()
        self.fields['megamenu_folder'].widgetFactory = RadioFieldWidget

        
   
class MegamenuSettingsFormWrapper(layout.FormWrapper):
    """Use this form as the plone.z3cform layout wrapper to get the control
    panel layout.
    """
    form = MegamenuSettingsEditForm
    index = ViewPageTemplateFile('templates/controlpanel.pt')
