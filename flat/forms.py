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
        fields = ['name', 'period']


class AnnouncementCreationForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['text']


class TodoForm(forms.Form):
    text = forms.CharField(max_length=40,
                           widget=forms.TextInput(
                                                  attrs={'class': 'form-control', 'placeholder': 'Enter what we need',
                                                         'aria-label': 'Todo', 'aria-describedby': 'add-btn'}))
