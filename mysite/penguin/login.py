from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    # UserCreationForm  does not include email attribute! 
    email = forms.EmailField(required=True)
    
    class Meta: # It's kinda like a inherited or super class
        model = User
        fields = ("username", "email", "password1", "password2")