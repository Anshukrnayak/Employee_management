
from django.urls import path
from app import views

urlpatterns = [

    path('',views.homePage,name='home'),
    path('leads/',views.ListLeads.as_view(),name='leads'),
    path('agent/',views.AgentProfile.as_view(),name='agent'),
    path('add_leads/',views.AddLeads.as_view(),name='add_leads'),
    path('leads_profile/<int:pk>/',views.LeadProfile.as_view(),name='lead_profile'),
    path('update_lead/<int:pk>',views.UpdateLead.as_view(),name='update_lead'),
    path('delete_lead/<int:pk>',views.DeletePage.as_view(),name='delete_lead'),
    path('agent_profile/',views.AgentView.as_view(),name='agent_profile'),


]
