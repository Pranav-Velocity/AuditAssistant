from django.contrib import admin
from .models import Act, Activity, Client, Industry, Regulator, Task, Entity, AuditType, ClientTask
from main_client.models import BillingDetails
# Register your models here.
admin.site.register(Regulator)
admin.site.register(Industry)
admin.site.register(AuditType)
admin.site.register(Entity)
admin.site.register(Act)
admin.site.register(Activity)
admin.site.register(Task)
admin.site.register(Client)
admin.site.register(ClientTask)
admin.site.register(BillingDetails)
