from django.urls import path
from . import views
urlpatterns = [
    path('',views.Dashboard,name="client_dashboard"),
    path('add_user/',views.AddUser,name="adduser"),
    path('files/',views.ShowFiles,name="showfiles"),
    path('reports/',views.ShowReports,name="show_main_client_reports"),
    path('export_excel/<str:employee_ids>', views.export_users_xls_mainclient, name='export_excel_mainclient'),
    path('export_pdf/<str:employee_ids>', views.export_pdf_mainclient, name='export_pdf_mainclient'),
    path('paymentsuccess', views.paymentsuccess, name='paymentsuccess'),
    path('paymentfailure', views.paymentfailure, name='paymentfailure'),
    
    
]