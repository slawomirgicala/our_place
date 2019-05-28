from django import forms
from .models import Flat, Chore, Announcement


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


class ChoreCreationForm(forms.ModelForm):
    class Meta:
        model = Chore
        fields = ['name']


class AnnouncementCreationForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['text']

