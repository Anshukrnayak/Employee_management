from django.urls import path
from account import views

urlpatterns = [
    path('login/',views.LoginView.as_view(),name='login'),
    path('signup/',views.SignupView.as_view(),name='signup'),
    path('logout/',views.logout_view,name='logout'),
    
]
