from django.urls import path, include

from .views import index, show_individual_task, start_task, end_task, task_submission,task_approval,tasks_status,all_task_tasks_status
from .views import start_working,rejected_task_remark,all_rejected_tasks_history,tasks_pending,article_dashboard
urlpatterns = [
    path('', article_dashboard, name="article_dashboard"),
    path('tasks', index, name="article_index"),
    path('task/<int:task_id>', show_individual_task, name='individual_task'),
    path('task/<int:task_id>/start', start_task, name="start_task"),
    path('task/<int:task_id>/end', end_task, name="end_task"),
    path('task/<int:task_id>/submit', task_submission, name="task_submission"),
    path('approval/<int:task_id>/submit', task_approval, name="task_approval"),
    path('task/status',tasks_status,name="tasks_status"),
    path('approvals/tasks/status',all_task_tasks_status,name="all_task_tasks_status"),
    path('start/working/<int:task_id>/submit',start_working,name="start_working"),
    path('remark/<int:task_id>/submit',rejected_task_remark,name="rejected_task_remark"),
    path('rejected/task',all_rejected_tasks_history,name="all_rejected_tasks_history"),
    path('approvals/pending',tasks_pending,name="tasks_pending")
   
   
]