from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','password1','password2']

    
    def __init__(self,*args,**kwargs):
        super(SignupForm,self).__init__(*args,**kwargs)
        self.fields['username'].widget.attrs['class']='w-full px-4 py-2 mt-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
        self.fields['password1'].widget.attrs['class']='w-full px-4 py-2 mt-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
        self.fields['password2'].widget.attrs['class']='w-full px-4 py-2 mt-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'