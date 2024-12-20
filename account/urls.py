
from django.urls import path
from account import views

urlpatterns = [

    path('login/',views.LoginPage.as_view(),name='login'),
    path('signup/',views.SignupPage.as_view(),name='signup'),
    path('logout/',views.logout_page,name='logout'),
    
    


]
