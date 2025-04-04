
from django.urls import path
from . import  views

urlpatterns=[

    path('',views.ClientView.as_view(),name='home'),
    path('create-client/',views.ClientCreate.as_view(),name='create_client'),
    path('update_client/<int:pk>/',views.ClientUpdateView.as_view(),name='update_client'),
    path('delete_client/<int:pk>/',views.ClientDeleteView.as_view(),name='delete_client'),

    # Leads
    path('leads/',views.LeadsView.as_view(),name='leads'),
    path('profile/',views.DisplayLeadProfile.as_view(),name='profile'),
    path('update-profile/<int:pk>/',views.UpdateLeadProfile.as_view(),name='edit_profile'),
    path('delete-profile/<int:pk>/',views.DeleteLeadProfile.as_view(),name='delete_profile'),


]

