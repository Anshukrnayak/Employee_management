
from django import forms
from app import models

class LeadForm(forms.ModelForm):
    class Meta:
        model=models.LeadModel
        fields=['image','name','location','contact','email','designation','experience','salary']


        widgets={
         
            'name':forms.TextInput(attrs={'class':' px-2 mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-gray-900'}),
            'contact':forms.TextInput(attrs={'class':' px-2 mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-gray-900'}),
            'email':forms.TextInput(attrs={'class':' px-2 mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-gray-900'}),
            'designation':forms.Select(attrs={'class':' px-2 mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-gray-900'}),
            'experience':forms.TextInput(attrs={'class':' px-2 mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-gray-900'}),
            'salary':forms.TextInput(attrs={'class':' px-2 mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-gray-900'}),
            'location':forms.TextInput(attrs={'class':' px-2 mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-gray-900'}),
         
        }