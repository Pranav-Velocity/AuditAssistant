from django.db import models
from datetime import datetime
from auditapp.models import User

class CAFirm(models.Model):
    ca_firm_name = models.CharField(max_length=255, null=False,blank=False)
    ca_firm_registration_id = models.CharField(max_length=255, null=False,blank=False)
    ca_firm_address = models.CharField(max_length=255, null=False,blank=False)

    ca_firm_pan = models.CharField(max_length=255, null=False,blank=False)
    ca_firm_tan = models.CharField(max_length=255, null=False,blank=False)

    # partner = models.ForeignKey(User, on_delete=models.SET_NULL, null=False, blank=False)

    def __str__(self):
        return self.ca_firm_name
    
# Create your models here.
