from django.urls import path, include
from . import views


urlpatterns = [
    path("",views.SuperAdminDashboard,name="super_admin_dashboard"),
    path("show_users",views.ShowUsers,name="show_users"),
    path('get_single_user/',views.GetSingleUser,name="get_single_user"),
    path('save_user/',views.SaveUser, name="save_user"),
    path('delete_user/',views.DeleteUser, name="delete_user"),
    path('add_main_client/',views.AddMainClient, name="add_main_client"),


    path('clients/',views.Clients,name="all_clients"),
    path('billing_details/',views.AddBillingDetails,name="all_billing_details"),
    path('main_client_reports/',views.MainClientReports,name="main_client_reports"),

    path('files/',views.FilesCreated,name="files_created"),
    path('export_excel/<str:employee_ids>', views.export_users_xls_superadmin, name='export_excel'),
    path('export_pdf/<str:employee_ids>', views.export_pdf_superadmin, name='export_pdf'),
    path('database',views.DatabaseMigrations,name="databasemigrations"),


    path('api/kunal/dashboard_super_admin/',views.DashboardSuperAdmin,name="dashboard_super_admin"),
    
]