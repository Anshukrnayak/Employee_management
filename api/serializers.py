
from app.models import ClientModel,LeadModel
from rest_framework import serializers


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model=ClientModel
        fields='__all__'


class LeadSerializer(serializers.ModelSerializer):

    clients=ClientSerializer(many=True)

    class Meta:
        model=LeadModel
        fields=['user','first_name','last_name','clients','location','profile_pic','about']
