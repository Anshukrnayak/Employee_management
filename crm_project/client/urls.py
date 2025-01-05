
from django.urls import path
from client import views

urlpatterns = [
    
    path('',views.ClientList.as_view(),name='clients'),
    path('add/',views.AddClient.as_view(),name='add_client'),
    path('detail/<int:pk>/',views.ClinetDetailView.as_view(),name='client_detail'),    
    path('edit-client/<int:pk>/',views.EditClientView.as_view(),name='edit_client'),
    path('delete-client/<int:pk>/',views.delete_client,name='delete_client'),

]


