from django.urls import path
from .views import *
urlpatterns = [
    path('',Dashboard,name="client_dashboard"),
    path('add_user/',AddUser,name="adduser"),
    path('files/',ShowFiles,name="showfiles"),
    path('reports/',ShowReports,name="show_main_client_reports"),
    path('export_excel/<str:employee_ids>', export_users_xls_mainclient, name='export_excel_mainclient'),
    path('export_pdf/<str:employee_ids>', export_pdf_mainclient, name='export_pdf_mainclient'),
    path('paymentsuccess', paymentsuccess, name='paymentsuccess'),
    path('paymentfailure', paymentfailure, name='paymentfailure'),


    path('client/setup', client_setup, name='client_setup'),
    path('clients/', render_client_master, name="client_master"),
    path('client/add', add_client, name="add_client"),
    path('client/<int:client_id>/profile', render_client_profile, name="client_profile"),
    path("client/<int:client_id>/tasks/",main_client_tasks,name="main_client_tasks"),


    path('client/auditplan/lock/<int:auditplan_id>', lock_audit_plan, name="lock_audit_plan"),
    path('client/auditplan/unlock/<int:auditplan_id>', unlock_audit_plan, name="unlock_audit_plan"),

    path('client/auditplan/add/<int:client_id>', add_audit_plan, name="add_audit_plan"),
    path('client/auditplan/<int:auditplan_id>', audit_plan, name="audit_plan"),
    
    path('areas/', render_areas_master, name="render_areas_master"),
    path('area/add', add_area, name='add_area'),
    path('area/delete/<int:area_id>', remove_area, name="remove_area"),
    path('area/edit', edit_area, name="edit_area"),
    path('area/make_global/<int:area_id>', area_make_global, name="area_make_global"),

    path('activitylabel/',render_activity_label_master,name="render_activity_label_master"),
    path('activitylabel/add', add_activitylabel, name='add_activitylabel'),
    path('activitylabel/edit', edit_activitylabel, name="edit_activitylabel"),
    path('activitylabel/delete/<int:activitylabel_id>', remove_activitylabel, name="remove_activitylabel"),
    path('activitylabel/make_global/<int:activitylabel_id>', activity_label_make_global, name="activity_label_make_global"),

    path('acts/', render_acts_master, name="render_acts_master"),
    path('act/add', add_act, name='add_act'),
    path('act/industries', get_industries, name="get_industries"), 
    path('act/delete/<int:act_id>', remove_act, name="remove_act"),
    path('act/edit', edit_act, name="edit_act"),
    path('act/make_global/<int:act_id>', acts_make_global, name="acts_make_global"),

    path('audittypes/', render_audittype_master, name="render_audittype_master"),
    path('audittype/add', add_audittype, name='add_audittype'),
    path('audittype/edit', edit_audittype, name="edit_audittype"),
    path('audittype/delete/<int:audittype_id>', remove_audittype, name="remove_audittype"),
    path('audittype/make_global/<int:audittype_id>', audit_type_make_global, name="audit_type_make_global"),

    path('entities/', render_entity_master, name="render_entity_master"),
    path('entity/add',add_entity,name='add_entity'),
    path('entity/edit', edit_entity, name="edit_entity"),
    path('entity/delete/<int:entity_id>', remove_entity, name="remove_entity"),
    path('entity/make_global/<int:entity_id>', entity_make_global, name="entity_make_global"),

    path('industries/', render_industry_master, name="render_industry_master"),
    path('industry/add', add_industry, name='add_industry'),
    path('industry/edit', edit_industry, name="edit_industry"),
    path('industry/delete/<int:industry_id>', remove_industry, name="remove_industry"),
    path('industry/make_global/<int:industry_id>', industry_make_global, name="industry_make_global"),

    path('audits/', render_audits_master, name="render_audits_master"),
    path('audits/add', add_audits, name='add_audits'),
    path('audits/edit', edit_audits, name="edit_audits"),
    path('audits/delete/<int:audit_id>', remove_audit, name="remove_audit"),
    path('audits/make_global/<int:audit_id>', audits_make_global, name="audits_make_global"),
    

    path('activities/', render_activity_master, name="render_activity_master"),
    path('activity/add', add_activity, name='add_activity'),
    path('activity/entities', get_entities, name="get_entities"),
    path('activity/delete/<int:activity_id>', remove_activity, name='remove_activity'),
    path('activity/edit1', edit_id_activity, name='edit_id_activity'),
    path('activity/edit', edit_activity, name="edit_activity"),
    path('activity/make_global/<int:activity_id>', activity_make_global, name="activity_make_global"),
    
    path('tasks/', render_task_master, name="render_task_master"),
    path('crud_processed_notes',crud_processed_notes,name="crud_processed_notes"),
    path('upload_task',upload_task,name="upload_task"),
    path('task/activities', get_activities, name="get_activities"),
    path('task/edit', edit_task, name="edit_task"),
    path('task/add', add_task, name="add_task"),
    path('task/delete/<int:task_id>', remove_task, name="remove_task"),
    path('task/make_global/<int:task_id>', task_make_global, name="task_make_global"),
    
    path('assign/<int:client_id>/', main_client_assign_task_to_employee, name="main_client_assign_task_to_employee"),
    path('get_all_managers/',get_all_managers,name="get_all_managers"),
    path('get_all_users/',get_all_users,name="get_all_users"),

]