from django import template
from partner.models import ClientTask
register = template.Library()

@register.filter()
def get_activity(task_id):
    return ClientTask.objects.filter(id=task_id).activity.get()