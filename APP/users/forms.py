from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django_registration.forms import RegistrationForm
from  django import  forms 
from .models import User


class RegistrationForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = User
        fields = ['email', 'full_name', 'country', 'National_id',"bio", 
                  'title', 'experience_level']


    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        #self.helper = FormHelper()
        #self.helper.add_input(Submit("submit", "Register"))



class UserUpdateForm(forms.ModelForm):
    class Meta:
      model = User
      fields = [ 'full_name', 'country', 'National_id',"bio", 
                  'title', 'experience_level']

        