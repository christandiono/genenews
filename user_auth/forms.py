from django.contrib.auth.forms import UserCreationForm as UCF
from django import forms
from django.contrib.auth.models import User

class UserCreationForm(UCF):
    email = forms.EmailField()

    def save(self):
        temp = super(UserCreationForm, self).save()
        temp.email = self.cleaned_data.get('email')
        temp.save()
