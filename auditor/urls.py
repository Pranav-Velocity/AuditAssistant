from django.urls import path, include

from .views import index, show_individual_task, start_task, end_task,auditor_task_submission,auditor_task_approval,auditor_tasks_status,auditor_all_task_tasks_status
from .views import auditor_start_working,auditor_rejected_task_remark,auditor_all_rejected_tasks_history,auditor_dashboard
from .views import approval_tasks_pending
urlpatterns = [
    path('',auditor_dashboard, name="auditor_dashboard"),
    path('tasks', index, name="auditor_index"),
    path('task/<int:task_id>', show_individual_task, name='auditor_individual_task'),
    path('task/<int:task_id>/start', start_task, name="start_task"),
    path('task/<int:task_id>/end', end_task, name="end_task"),
    path('task/<int:task_id>/submit', auditor_task_submission, name="auditor_task_submission"),
    path('approval/<int:task_id>/submit',auditor_task_approval, name="auditor_task_approval"),
    path('task/status',auditor_tasks_status,name="auditor_tasks_status"),
    path('approvals/tasks/status',auditor_all_task_tasks_status,name="auditor_all_task_tasks_status"),
    path('start/working/<int:task_id>/submit',auditor_start_working,name="auditor_start_working"),
    path('remark/<int:task_id>/submit',auditor_rejected_task_remark,name="auditor_rejected_task_remark"),
    path('rejected/task',auditor_all_rejected_tasks_history,name="auditor_all_rejected_tasks_history"),
    path('approvals/pending',approval_tasks_pending,name='approval_tasks_pending')
   
]