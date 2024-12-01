from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    
    path('',views.Home_page.as_view(),name='home'),
    path('employee-form/',views.employee_form.as_view(),name='employee_form'),
    path('delete/<int:pk>',views.delete_employee,name='delete'),
    path('update/<int:pk>',views.employee_update.as_view(),name='update')


]
