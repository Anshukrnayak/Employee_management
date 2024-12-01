from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    
    path('signup/',views.singup_page.as_view(),name='signup'),
    path('login/',views.Login_page.as_view(),name='login'),
    path('logout/',views.logout_page,name='logout'),
    

]
