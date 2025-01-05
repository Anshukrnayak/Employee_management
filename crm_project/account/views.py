from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from account.forms import SignupForm

class LoginView(View):
    def get(self,request,*args,**kwargs):
        return render(request,'account/login.html')


    def post(self,request,*args,**kwargs):

        try:
            username=request.POST['username']
            password=request.POST['password']

            print(f'username is : {username}')
            print(f'password is : {password}') 

            user=authenticate(username=username,password=password)
            print(f'{user}')
            if user is not None:
                print('user is not none')
                login(request,user)
                messages.info(request,'user login successfully')
                return redirect('home')

            messages.error(request,'please enter correct username or password ')
            return redirect('login')

        except:
            messages.error(request,'please fill crendtial ')
            return redirect('login')


class SignupView(View):
    def get(self,request,*args,**kwargs):
        form=SignupForm()
        return render(request,'account/signup.html',{'form':form})

    def post(self,request):

        form=SignupForm(data=request.POST)
        
        if form.is_valid():
            form.save()
            print('valid form ')
            messages.info(request,'New user created successfully')
            return redirect('login')

        return render(request,'account/signup.html',{'form':form})


@login_required
def logout_view(request):
    logout(request)

    messages.info(request,'user successfully logout')
    return redirect('home')    

