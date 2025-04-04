
from django import forms
from .models import LeadModel, ClientModel

class LeadForm(forms.ModelForm):
    class Meta:
        model = LeadModel
        fields = ['first_name', 'last_name', 'location', 'about', 'profile_pic']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded', 'placeholder': 'Last Name'}),
            'location': forms.Textarea(attrs={'class': 'w-full p-2 border border-gray-300 rounded', 'placeholder': 'Location', 'rows': 3}),
            'about': forms.Textarea(attrs={'class': 'w-full p-2 border border-gray-300 rounded', 'placeholder': 'About', 'rows': 3}),
            'profile_pic': forms.FileInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}),
        }

class ClientForm(forms.ModelForm):
    class Meta:
        model = ClientModel
        fields = ['first_name', 'last_name', 'location', 'status', 'about', 'contact', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded', 'placeholder': 'Last Name'}),
            'location': forms.Textarea(attrs={'class': 'w-full p-2 border border-gray-300 rounded', 'placeholder': 'Location', 'rows': 3}),
            'about': forms.Textarea(attrs={'class': 'w-full p-2 border border-gray-300 rounded', 'placeholder': 'About', 'rows': 3}),
            'contact': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded', 'placeholder': 'Contact'}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded', 'placeholder': 'Email'}),
            'status': forms.Select(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}),
        }
