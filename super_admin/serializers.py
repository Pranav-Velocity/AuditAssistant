from rest_framework import serializers
from main_client.models import MaxFiles,MaxUsers,BillingDetails
from partner.models import Regulator,UserLink, Act, Activity, Industry, Task, Client, Entity, AuditType, ActivityAuditTypeEntity, ClientIndustryAuditTypeEntity,AuditPlanMapping



class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class BillingDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingDetails
        fields = '__all__'