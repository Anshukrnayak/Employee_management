from django.shortcuts import render,redirect
from django.views import  generic
from .forms import SignupForm,LoginForm
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.mixins import LoginRequiredMixin

# signup view :
class RegisterView(generic.View):
    def get(self,request):
        form=SignupForm()
        return render(request,'account/register.html',{'form':form})

    def post(self,request):
        form=SignupForm(data=request.POST)
        if form.is_valid():
            login(request,form.save())
            return redirect('create_lead')
        return render(request,'account/register.html',{'form':form})


class LoginView(generic.View):
    def get(self,request):
        form=LoginForm()
        return render(request,'account/login.html',{'form':form})

    def post(self,request):
        form=LoginForm()

        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            form.add_error(None, 'Invalid username or password')
        return render(request,'account/login.html',{'form':form})


class LogoutView(LoginRequiredMixin,generic.View):
    def get(self,reqeust):
        logout(reqeust)
        return redirect('home')

