from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import  User

class SignupForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','password1','password2']

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': field.label
            })

class LoginForm(forms.Form):
    username = forms.CharField(
        label='Username',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded',
            'placeholder': 'Enter your username'
        })
    )

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded',
            'placeholder': 'Enter your password'
        })
    )
