from django.urls import path
from app import views

urlpatterns = [
    path('',views.home_page,name='home'),
    path('setting/',views.setting_view,name='setting'),
    

]
