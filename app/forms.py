
from app.models import LeadModel
from django import forms


class LeadForm(forms.ModelForm):
    class Meta:
        model=LeadModel
        fields=['profile_image','name','email','contact']


        widgets={
            'name':forms.TextInput(attrs={'class':'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500'}),
            'contact':forms.NumberInput(attrs={'class':'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500'}),
            'email':forms.EmailInput(attrs={'class':'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500'})
        
        }        



