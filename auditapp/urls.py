
from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings
from .views import index

urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
    
    path('developers_console/',include('dev_admin.urls')),
    path('superadmin/',include('super_admin.urls')),
    path('accounts/',include('django.contrib.auth.urls')),
    path('main_client/',include('main_client.urls')),
    path('partner/', include('partner.urls')),
    path('manager/', include('manager.urls')),
    path('auditor/', include('auditor.urls')),
    path('article/', include('articleholder.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)







