from django.urls import path, include

from .views import index,show_individual_task,task_unapproved,manager_task,assign_task_to_employee,approved_tasks,all_task_status,manager_tasks,show_individual_manager_task
from .views import rejected_tasks,reassign_task,manager_dashboard, assign_multiple_task,list_of_clients,client_tasks
from manager.views import approval_pending_tasks,is_rejected_tasks,start_task,end_task,manager_task_submission,manager_start_working,manager_rejected_task_remark
urlpatterns = [
    path('',manager_dashboard,name="manager_dashboard"),
    path('tasks/status', index, name="manager_index"),
    path('approval/<int:task_id>', show_individual_task, name='approval'),
    path('unapproved/<int:task_id>/submit', task_unapproved, name="task_unapproved"),
    path('approved/<int:task_id>/submit',approved_tasks,name="approved_tasks"),
    path('assign_tasks',manager_task,name='manager_task'),

    path('tasks',manager_tasks,name='manager_tasks'),
    path('task/<int:task_id>', show_individual_manager_task, name='individual_manager_task'),
    path('task/<int:task_id>/start', start_task, name="start_task"),
    path('task/<int:task_id>/end', end_task, name="end_task"),
    path('start/working/<int:task_id>/submit',manager_start_working,name="manager_start_working"),
    path('remark/<int:task_id>/submit',manager_rejected_task_remark,name="manager_rejected_task_remark"),
    path('task/<int:task_id>/submit', manager_task_submission, name="manager_task_submission"),     


    path('assign/<int:client_id>/', assign_task_to_employee, name="assign_task_to_employee"),
    path('all/tasks/status',all_task_status,name="all_task_status"),
    path('rejected/task<int:task_id>/submit',rejected_tasks,name="rejected_tasks"),
    path('reassign/<int:client_id>/tasks/',reassign_task ,name="reassign_task"),
    path('assign/<int:client_id>/multiple',assign_multiple_task, name="assign_multiple_tasks"),
    path("clients/list",list_of_clients,name="list_of_clients"),
    path("client/<int:client_id>/tasks/",client_tasks,name="client_tasks"),
    path("rejected/tasks",is_rejected_tasks,name="is_rejected_tasks"),
    path("pendings/approvals/tasks",approval_pending_tasks,name="approval_pending_tasks"),


]       