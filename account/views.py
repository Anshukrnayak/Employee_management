from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import login,logout
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate

class singup_page(View):

    def get(self,request):

        form=UserCreationForm()

        return render(request,'account/signup.html',{'form':form})
    

    def post(self,request):


        form=UserCreationForm(data=request.POST)

        if form.is_valid():
            login(request,user)

            return  redirect('home')
        

        return render(request,'account/signup.html',{'form':form})



class Login_page(View):


    def get(self,request):


        form=AuthenticationForm()
        

        return render(request,'account/login.html',{'form':form})

    
    def post(self,request):

        form=AuthenticationForm(data=request.POST)
        

        if form.is_valid():

            username=form.cleaned_data['username']
            password=form.cleaned_data['password']

            user=authenticate(username=username,password=password)

            if user is not None: 
                login(request,user)
                return redirect('home')


        return render(request,'account/login.html',{'form':form})


@login_required
def logout_page(request):

    logout(request)

    return redirect('home')
