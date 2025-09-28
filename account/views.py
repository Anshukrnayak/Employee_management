from django.shortcuts import render, redirect
from django.views import generic
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.urls import reverse_lazy
from .forms import SignupForm, LoginForm
from django.contrib.auth.mixins import AccessMixin


class AnonymousRequiredMixin(AccessMixin):
    """Verify that the current user is anonymous."""
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, 'You are already logged in.')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)


class RegisterView(AnonymousRequiredMixin,generic.View):
    """User registration view with improved error handling and security"""

    # Use reverse_lazy for URLs to avoid circular imports
    success_url = reverse_lazy('create_lead')
    template_name = 'account/register.html'

    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        # Redirect authenticated users away from registration page
        if request.user.is_authenticated:
            messages.info(request, 'You are already logged in.')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = SignupForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = SignupForm(request.POST)

        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, 'Account created successfully! Welcome!')
                return redirect(self.success_url)
            except Exception as e:
                # Log the exception in production (you might want to use logging)
                messages.error(request, 'An error occurred during registration. Please try again.')
        else:
            messages.error(request, 'Please correct the errors below.')

        return render(request, self.template_name, {'form': form})


class LoginView(AnonymousRequiredMixin,generic.View):
    """User login view with improved security and error handling"""

    success_url = reverse_lazy('home')
    template_name = 'account/login.html'

    @method_decorator(csrf_protect)
    @method_decorator(sensitive_post_parameters('password'))
    def dispatch(self, request, *args, **kwargs):
        # Redirect authenticated users away from login page
        if request.user.is_authenticated:
            messages.info(request, 'You are already logged in.')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')

                # Optional: Redirect to next parameter if present
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect(self.success_url)

        # If we get here, authentication failed
        messages.error(request, 'Invalid username or password.')
        return render(request, self.template_name, {'form': form})


class LogoutView(LoginRequiredMixin, generic.View):
    """User logout view with improved handling"""

    success_url = reverse_lazy('home')

    def get(self, request):
        # Use POST requests for logout in production for better security
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect(self.success_url)

    def post(self, request):
        """POST method for logout (more secure)"""
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect(self.success_url)