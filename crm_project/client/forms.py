from django import forms
from app.models import ClientModel



class ClientForm(forms.ModelForm):
    class Meta:
        model=ClientModel
        fields=['image','name','location','contact','email','status','description']


        widgets={
            
            'name':forms.TextInput(attrs={'class':' px-2 mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-gray-900'}),
            'location':forms.TextInput(attrs={'class':'px-2mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-gray-900'}),
            'email':forms.EmailInput(attrs={'class':'px-2 mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-gray-900'}),
            'status':forms.Select(attrs={'class':'px-2 mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-gray-900'}),
            'contact':forms.NumberInput(attrs={'class':'px-2 mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-gray-900'}),
            'description':forms.Textarea(attrs={'class':'px-2 mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-gray-900'}),
            
        }

