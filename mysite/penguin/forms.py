# myapp/forms.py

from django import forms
from .models import Player

class forms(forms.ModelForm):
    class Meta:
        model = Player
        fields = ('username',)