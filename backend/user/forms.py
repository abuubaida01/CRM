from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User
from django.contrib.auth import forms as auth_forms
from django import forms


# https://www.geeksforgeeks.org/python-extending-and-customizing-django-allauth/
# https://django-allauth.readthedocs.io/en/latest/forms.html

# from allauth.account.forms import SignupForm
from django import forms
# from allauth.account.forms import AddEmailForm
from django.forms.widgets import DateInput



# religion = [
#     ('Muslim', 'Muslim'),
#     ('Christian', 'Christian'),
#     ('Jew', 'Jew'),
#     ('Hindu', 'Hindu'),
#     ('Sikh', 'Sikh'),
#     ('Buddhist', 'Buddhist'),
#     ('Agnostic', 'Agnostic'),
#     ('Atheist', 'Atheist'),
#     ('Other', 'Other'),
# ]

religion = [
  ('Islam', 'Islam'),
  ('Christianity', 'Christianity'),
  ('Judaism', 'Judaism'),
  ('Hinduism', 'Hinduism'),
  ('Sikhism', 'Sikhism'),
  ('Buddhism', 'Buddhism'),
  ('Agnosticism', 'Agnosticism'),
  ('Atheism', 'Atheism'),
  ('Other', 'Other'),
] 



gender = [
  ('Male','Male'),
  ('Female', 'Female'),
]

# class CustomSignupForm(SignupForm):
#   name = forms.CharField(max_length=30, label='Full Name', required=True, widget=forms.TextInput(attrs={'placeholder': 'Full Name'}))

#   religion = forms.CharField(max_length=30, label='Religion', required=True, widget=forms.Select(choices=religion, attrs={'placeholder': 'Select your Religion'}))

#   gender = forms.CharField(max_length=30, label='Gender', required=True, widget=forms.Select(choices=gender,  attrs={'placeholder': 'Select your Gender'}))

#   date_of_birth = forms.DateField(label='Date of Birth', required=True, widget=DateInput(attrs={'type': 'date'}))

#   def save(self, request):
#       user = super(CustomSignupForm, self).save(request)
#       user.full_name = self.cleaned_data['name']
#       user.religion = self.cleaned_data['religion']
#       user.gender = self.cleaned_data['gender']
#       user.date_of_birth = self.cleaned_data['date_of_birth']

#       user.save()
#       return user 


class UserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email',) 



class UserChangeForm(auth_forms.UserChangeForm):
    password = auth_forms.ReadOnlyPasswordHashField(label="Password")
    class Meta:
        model = User
        fields = ['full_name','username'] 
        