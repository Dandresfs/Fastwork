from crispy_forms.helper import FormHelper
from accounts.models import User

class AspiranteFilterFormHelper(FormHelper):
    model = User
    form_tag = False