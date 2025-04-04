from django.urls import path,include
from . import  views
from rest_framework.routers import DefaultRouter

route=DefaultRouter()

route.register('lead/',views.LeadViewSet,basename='lead')
route.register('client/',views.ClientViewSet,basename='client')

urlpatterns=[
    path('',include(route.urls))
]


