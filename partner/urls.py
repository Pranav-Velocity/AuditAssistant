from django.urls import path, include

# Import Index route
from .views import index, invoice_details, partner_dashboard
from .views import *

from .views import  remove_client,view_client_activitiess,assign_task_to_employee,edit_client,get_clientdetails
from .views import clone_client
from .views import list_clients_setup
from .views import Reports , add_client_task
# from .views import employee_setup,add_employee, edit_employee
from .views import mapping
from partner.views import partner_approval_pending_tasks,pending_approval_task,approve_tasks,reject_task,partner_list_of_clients,partner_client_tasks,partner_assign_task_to_employee
from partner.views import partner_tasks,show_individual_partner_task,partner_start_working,partner_task_submission,view_client_invoicing,client_invoice_download,edit_invoice,invoice_details,create_invoice,partner_dashboard
from .views import test
urlpatterns = [
    # path('test/',test,name="test"),
    path('', index, name="partner_index"),
    path('dashboard', partner_dashboard, name="partner_dashboard"),

    # path('areas/', render_areas_master, name="render_areas_master"),
    # path('area/add', add_area, name='add_area'),
    # path('area/delete/<int:area_id>', remove_area, name="remove_area"),
    # path('area/edit', edit_area, name="edit_area"),

    # path('activitylabel/',render_activity_label_master,name="render_activity_label_master"),
    # path('activitylabel/add', add_activitylabel, name='add_activitylabel'),
    # path('activitylabel/edit', edit_activitylabel, name="edit_activitylabel"),
    # path('activitylabel/delete/<int:activitylabel_id>', remove_activitylabel, name="remove_activitylabel"),

    # path('acts/', render_acts_master, name="render_acts_master"),
    # path('act/add', add_act, name='add_act'),
    # path('act/industries', get_industries, name="get_industries"), 
    # path('act/delete/<int:act_id>', remove_act, name="remove_act"),
    # path('act/edit', edit_act, name="edit_act"),

    # path('audittypes/', render_audittype_master, name="render_audittype_master"),
    # path('audittype/add', add_audittype, name='add_audittype'),
    # path('audittype/edit', edit_audittype, name="edit_audittype"),
    # path('audittype/delete/<int:audittype_id>', remove_audittype, name="remove_audittype"),

    # path('entities/', render_entity_master, name="render_entity_master"),
    # path('entity/add',add_entity,name='add_entity'),
    # path('entity/edit', edit_entity, name="edit_entity"),
    # path('entity/delete/<int:entity_id>', remove_entity, name="remove_entity"),

    # path('industries/', render_industry_master, name="render_industry_master"),
    # path('industry/add', add_industry, name='add_industry'),
    # path('industry/edit', edit_industry, name="edit_industry"),
    # path('industry/delete/<int:industry_id>', remove_industry, name="remove_industry"),

    # path('activities/', render_activity_master, name="render_activity_master"),
    # path('activity/add', add_activity, name='add_activity'),
    # path('activity/entities', get_entities, name="get_entities"),
    # path('activity/delete/<int:activity_id>', remove_activity, name='remove_activity'),
    # path('activity/edit1', edit_id_activity, name='edit_id_activity'),
    # path('activity/edit', edit_activity, name="edit_activity"),
    
    # path('tasks/', render_task_master, name="render_task_master"),
    # path('crud_processed_notes',crud_processed_notes,name="crud_processed_notes"),
    # path('upload_task',upload_task,name="upload_task"),
    # path('task/activities', get_activities, name="get_activities"),
    # path('task/edit', edit_task, name="edit_task"),
    # path('task/add', add_task, name="add_task"),
    # path('task/delete/<int:task_id>', remove_task, name="remove_task"),
    path('email/<int:client_id>', assign_task_to_employee,name="assign_task_to_employee"),
    path("pendings/approvals/tasks",partner_approval_pending_tasks,name="partner_approval_pending_tasks"),
    path('approval/<int:task_id>', pending_approval_task, name='pending_approval_task'),
    path('approve/<int:task_id>/submit',approve_tasks,name="approve_tasks"),
    path('reject/task<int:task_id>/submit',reject_task,name="reject_task"),

    # path('tasks',partner_client_task,name='partner_client_task'),
    path('assign/<int:client_id>/', partner_assign_task_to_employee, name="partner_assign_task_to_employee"),
    path("clients/list",partner_list_of_clients,name="partner_list_of_clients"),
    path("client/<int:client_id>/tasks/",partner_client_tasks,name="partner_client_tasks"),

    path("assign_manager/",assign_manager,name="assign_manager"),

    
    path('client/delete/<int:client_id>',remove_client,name="remove_client"),
    path('client/<int:client_id>/tasks', view_client_activitiess, name="view_client_activitiess"),
    path('client/clone', clone_client, name="clone_client"),

    path('client/<int:client_id>/task/add', add_client_task, name="add_client_task"),
    path('assign/clients/lists/', list_clients_setup, name="list_clients_setup"),
    
    path('client/mapping',mapping,name="mapping"),
    path('client/edit', edit_client, name="edit_client"),
    path('client/clientdetails', get_clientdetails, name="get_clientdetails"),

    path('client/<int:client_id>/invocing',view_client_invoicing,name="view_client_invoicing"),
    path('client/<int:client_id>/invocing/create',create_invoice,name="create_invoice"),
    path('client/invocing/edit',edit_invoice,name="edit_invoice"),
    path('client/invocing/details', invoice_details, name="invoice_details"),
    path('client/<int:auditplan_id>/download',client_invoice_download,name="client_invoice_download"),

    # path('employee/setup',employee_setup,name="employee_setup"),
    # path('employee/add', add_employee, name="add_employee"),
    # path('employee/edit', edit_employee, name="edit_employee"),


    path('my_tasks/', partner_tasks, name="partner_tasks"),
    path('my_task/<int:task_id>', show_individual_partner_task, name='show_individual_partner_task'),
    path('start/working/<int:task_id>/submit',partner_start_working,name="partner_start_working"),
    path('my_task/<int:task_id>/submit', partner_task_submission, name="partner_task_submission"), 


    path('reports/',Reports, name='reports'),
    path('export_excel/<str:employee_ids>', export_users_xls_partner, name='export_excel_partner'),
    path('export_pdf/<str:employee_ids>', export_pdf_partner, name='export_pdf_partner'),
]