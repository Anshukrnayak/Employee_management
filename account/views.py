from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.views import generic,View
from .forms import SignupForm
from django.contrib import messages
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate

class LoginPage(View):

    def get(self,request):
    
        return render(request,'account/login.html')

    def post(self,request):

        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            messages.info(request,'Login successfully ')

            return redirect('home')

        messages.error(request,'please check username or password ')

        return render(request,'account/login.html')




class SignupPage(View):

    def get(self,request):
        form=SignupForm
        return render(request,'account/signup.html',{'form':form})

    def post(self,request):

        form=SignupForm(data=request.POST)

        if form.is_valid():
            login(request,form.save())
          
            messages.info(request,'You account created successfully...')
    
            return redirect('agent_profile')
        
        return render(request,'account/signup.html',{'form':form})


def logout_page(request): 

    logout(request)

    messages.info(request,'User logout successfully')
    return redirect('home')



