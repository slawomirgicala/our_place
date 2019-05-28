from django import forms
from .models import Flat


class FlatCreationForm(forms.ModelForm):
    class Meta:
        model = Flat
        fields = ['name', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }


class EnterFlatCreationForm(forms.ModelForm):
    class Meta:
        model = Flat
        fields = ['name', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

