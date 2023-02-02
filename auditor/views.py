from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from auditapp.models import User
from partner.models import Task, Client, ClientTask
from datetime import timedelta, date , datetime
from main_client.models import MaxUsers,MaxFiles
from django.http import JsonResponse
from django.conf import settings
import os
from django.core.files.base import ContentFile
import json
# Create your views here.
@login_required
def auditor_dashboard(request):
    if request.user.is_auditorclerk:
        if request.method == "POST":
            task_id_notification_seen = request.POST.get('task_id_notification_seen')
            if task_id_notification_seen:
                try:
                    get_client_task = ClientTask.objects.get(id = task_id_notification_seen)
                    get_client_task.notification = True
                    get_client_task.save()
                    print("yes got client task")
                    return JsonResponse({'saved':'yes'})
                except ClientTask.DoesNotExist:
                    pass
        all_tasks = ClientTask.objects.filter(user=request.user.id,is_approved=False,is_rejected=False,status=False).count()
        all_approved_tasks = ClientTask.objects.filter(user=request.user.id,is_approved=True).count()
        all_rejected_tasks = ClientTask.objects.filter(user=request.user.id,is_rejected=True).count()
        approval_pending = ClientTask.objects.filter(user=request.user.id,is_approved=False,status=True).count()
        pending_to_start_task=ClientTask.objects.filter(status=False,is_start=False,is_approved=False,user=request.user)
        message = ""
        client_task_id = ""
        url = ""
        for i in pending_to_start_task:
            if i.notification == False:
                message = "New task added. Please check task ."
                client_task_id = i.id
                url = "/auditor/tasks"
        context_set={
                    'all_approved_tasks':all_approved_tasks,
                    'all_rejected_tasks':all_rejected_tasks,
                    'all_tasks':all_tasks,
                    'approval_pending':approval_pending,
                    "message":message,
                    "client_task_id":client_task_id,
                    "url":url
                    }
        return render(request,"auditor/auditor_dashboard.html",context_set)

@login_required
def index(request):
    if request.user.is_auditorclerk:
        current_user = request.user

        assigned_tasks = ClientTask.objects.filter(user__id=current_user.id,status=False,is_approved=False,is_rejected=False)
        print(assigned_tasks)
        
        context_data = {
            'assigned_tasks': assigned_tasks
        }
        return render(request,"auditor/auditor_index.html", context_data)

@login_required
def show_individual_task(request, task_id):
    if request.user.is_auditorclerk:
        task = ClientTask.objects.get(id = task_id)
        client = Client.objects.get(id = task.client_id)

        estimated_end_date = None
        in_time = False
        if task.task_start_datetime is not None and task.task_end_datetime is not None:
            estimated_end_date = task.task_start_datetime + timedelta(minutes = int(task.task_estimated_days))
            print("result 4 :",estimated_end_date , int(task.task_estimated_days))
            in_time = True

            if estimated_end_date < task.task_end_datetime:
                in_time = False
        # print(in_time)
        file_location = ""
        if task.auditor_attachment_file: 
            str_data = task.auditor_attachment_file.replace("'",'"')
            json_data = json.loads(str_data)
            file_location = json_data['file_location']
        context_data = {
            'task': task, 
            'client': client,
            'estimated_end_date': estimated_end_date,
            'in_time': in_time,
            "file_location":file_location,
            "estimated_time":str(int(task.task_estimated_days)  // 60) + ":" + str(int(task.task_estimated_days)  % 60)
        }
        print(context_data)
        return render(request,'auditor/individual_task.html',context_data)

@login_required
def start_task(request, task_id):
    if request.user.is_auditorclerk:
        task = ClientTask.objects.get(id = task_id)
        
        try:
            # Update start date as current date
            task.task_start_date = date.today()

            # Update End date to Start date + estimated days
            task.task_end_date = date.today() + timedelta(days = int(task.task_estimated_days))
            task.save()
        except Exception as e:
            print(e)
        

        return HttpResponseRedirect('/auditor/task/{}'.format(task_id))

@login_required
def end_task(request, task_id):
    if request.user.is_auditorclerk:
        task = ClientTask.objects.get(id = task_id)
        
        try:
            # Update start date as current date
            task.task_end_date = date.today()
            task.save()

        except Exception as e:
            print(e)
        
        return HttpResponseRedirect('/auditor/task/{}'.format(task_id))

@login_required
def auditor_task_submission(request, task_id):
    if request.user.is_auditorclerk:
        try:
            getuser = User.objects.get(id=request.user.id)
            print(getuser)
        except User.DoesNotExist:
            getuser = "none"
        if request.method == "POST":            
            task = ClientTask.objects.get(id = task_id)
            try:
                uploaded_attachment_filename = request.FILES[u'attachment'].name
                uploaded_attachment_file = request.FILES['attachment']
                uploaded_attachment_filename = str(task_id) + "/" +  uploaded_attachment_filename
                print(" Uploaded File with no folder creation",uploaded_attachment_filename)

                # task.attachment_file.save(uploaded_attachment_filename, uploaded_attachment_file)
                # # task.attachment_file = request.FILES['attachment']
                # task.remark = request.POST.get('remark')
                # task.status = True
                # task.is_rejected = False
                # # task.save()
                if uploaded_attachment_file:
                    print("attachment got :")
                    if getuser == "none":
                        pass
                    else:
                        main_client = User.objects.get(id = getuser.linked_employee)
                        print(main_client)
                        try:
                            get_max_files = MaxFiles.objects.get(main_client = main_client.id)
                            if int(get_max_files.current_files) == int(get_max_files.max_files):
                                print("error files exceeded limit")
                            else:
                                path = str(settings.MEDIA_ROOT) + '\\clients\\'+ str(main_client.username) + '\\'
                                directory = 'task_submission'
                                dire = os.path.join(path, directory)
                                print(dire) 

                                uploaded_filename = request.FILES['attachment'].name
                                try:
                                    os.makedirs(dire)
                                    print("created folder")
                                except:
                                    print("folder already created")
                                    pass
                                task_file_upload_path = str(dire) + '\\'+str(task_id) + '\\' + 'auditor' +'\\'
                                try:
                                    os.makedirs(task_file_upload_path)
                                    print("created folder")
                                except:
                                    print("folder already created")
                                    pass
                                full_filename = os.path.join(task_file_upload_path, uploaded_filename)
                                fout = open(full_filename, 'wb+')
                                print("full_filename :",full_filename)
                                file_content = ContentFile( request.FILES['attachment'].read() )
                                # Iterate through the chunks.
                                for chunk in file_content.chunks():
                                    fout.write(chunk)
                                fout.close()
                                remove_absolute_path = full_filename.replace(str(settings.MEDIA_ROOT),'')
                                print("removed path :",remove_absolute_path)
                                # task.auditor_attachment_file.name = remove_absolute_path
                                task.auditor_attachment_file =  {
                                "user_id":f"{request.user.id}",
                                "file_location":f"{remove_absolute_path}"
                                }
                                get_max_files.current_files = int(get_max_files.current_files) + 1
                                get_max_files.save()
                        except MaxFiles.DoesNotExist:
                            print("no max files found")
                        task.remark = request.POST.get('remark')
                        task.status = True
                        task.is_rejected = False
                        task.save()

            except Exception as e:
                print(e)
            
        return HttpResponseRedirect('/auditor/task/{}'.format(task_id))

#Task Status
@login_required
def auditor_task_approval(request,task_id):
    if request.user.is_auditorclerk:
        task = ClientTask.objects.filter(id=task_id).update(status=True)
    return HttpResponseRedirect('')

def auditor_start_working(request,task_id):
    if request.user.is_auditorclerk:
        task= ClientTask.objects.get(id=task_id)
        task.is_start = True
        task.task_start_date = date.today()
        task.task_start_datetime = datetime.now()
        task.is_rejected = False
        task.save()
        print(date.today())
        return HttpResponseRedirect(f'/auditor/task/{task_id}')


def auditor_all_task_tasks_status(request):
    if request.user.is_auditorclerk:
        current_user = request.user
        approvals_tasks = ClientTask.objects.filter(user__id=current_user.id,is_approved=True,status=True)
        
        context={

        'approvals_tasks':approvals_tasks
    }   
        return render(request,"auditor/auditor_approval_tasks_status.html",context)


def auditor_tasks_status(request):
    if request.user.is_auditorclerk:
        return render(request,"auditor/auditor_tasks_status.html")   


def auditor_rejected_task_remark(request,task_id):
    if request.user.is_auditorclerk:
        if request.method == 'POST':
            remark_data = request.POST.get('remark')
            task = ClientTask.objects.filter(id=task_id).update(rejection_remark=remark_data)
            task_rejected = ClientTask.objects.filter(id=task_id).update(is_reject=True)
    return HttpResponseRedirect("/auditor/rejected/task")   


def auditor_all_rejected_tasks_history(request):
    if request.user.is_auditorclerk:
        current_user = request.user
        auditor_rejected_tasks = ClientTask.objects.filter(user__id=current_user.id).filter(is_rejected=True)
        context = {
            'auditor_rejected_tasks': auditor_rejected_tasks
        }
        return render(request,"auditor/rejected_tasks_by_auditor.html",context)

def approval_tasks_pending(request):
    all_pending_task = ClientTask.objects.filter(user__id=request.user.id,is_approved=False,status=True)
    return render(request,'auditor/approvals_pending_tasks.html',{'all_pending_task':all_pending_task})