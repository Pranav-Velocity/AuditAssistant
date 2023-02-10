import datetime
from datetime import timedelta, date
from django import template
import locale
from babel.numbers import format_currency
from partner.models import ClientTask
register = template.Library()

@register.filter()
def add_days(value, days):
    return value + datetime.timedelta(days=int(days))
 
@register.filter()
def currency(value):
    # v = float(value)
    # print("VALUE:" ,type(v))
    return format_currency(value, 'INR', locale='en_IN')

@register.filter
def div(value, arg):
    if arg == None:
        arg = 0
    try:
        if value:
            return float(value) * float(arg/100)
        else:
            return 0
    except (ValueError, ZeroDivisionError):
        return 0

@register.filter
def subtract(value, arg):
    return value - arg

@register.filter
def time_taken(task_id):
    task = ClientTask.objects.get(id = task_id)
    in_time = False
    if task.task_start_datetime is not None and task.task_end_datetime is not None:
        estimated_end_date = task.task_start_datetime + timedelta(minutes = int(task.task_estimated_days))
        print("result 4 :",estimated_end_date , int(task.task_estimated_days))
        in_time = True

        if estimated_end_date < task.task_end_datetime:
            in_time = False
        if in_time == True:
            color = "green"
        else:
            color = "red"
    return in_time

@register.filter
def prog(value, arg):
    if value !=0 and arg !=0:
        return round((float(value) / (float(arg) )) * 100,2)
    else:
        return 0

@register.filter
def prog2(value, arg):
    if value !=0 and arg !=0:
        return round(100 - (float(value) / (float(value) + float(arg))) * 100,2)
    else:
        return 0