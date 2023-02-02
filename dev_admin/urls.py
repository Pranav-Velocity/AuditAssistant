from django.urls import path

from .views import index,createnewcafirm,casetup
urlpatterns = [
    path('', index, name='index'),
    path('ca_setup/', casetup,name='casetup'),
    path('createdb/', createnewcafirm, name='createnewcafirm'),
]