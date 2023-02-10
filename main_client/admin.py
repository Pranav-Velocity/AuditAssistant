from django.contrib import admin
from .models import MaxUsers,MaxFiles
# Register your models here.
admin.site.register(MaxUsers)
admin.site.register(MaxFiles)