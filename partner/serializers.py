from rest_framework import serializers
from main_client.models import MaxFiles,MaxUsers,BillingDetails
from partner.models import ClientTask



class ClientTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientTask
        fields = '__all__'

