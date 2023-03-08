from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from auditapp.models import User
from partner.models import ClientTask as Task, Client,ClientTask
from main_client.models import MaxUsers,MaxFiles
from django.conf import settings
import os
from django.core.files.base import ContentFile
from datetime import timedelta, date ,datetime
from django.http import JsonResponse
# Create your views here.
from django.db.models import Count
import json
from super_admin.views import FilesStorage

@login_required
def article_dashboard(request):
    if request.user.is_articleholder:
        
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
        all_tasks = ClientTask.objects.filter(user=request.user.id,is_approved=False,is_reject=False,is_rejected=False,status=False).count()
        all_approved_tasks = ClientTask.objects.filter(user=request.user.id,is_approved=True).count()
        all_rejected_tasks = ClientTask.objects.filter(user=request.user.id,is_rejected=True).count()
        pending_tasks = ClientTask.objects.filter(user=request.user.id,is_approved=False,status=True).count()
        pending_to_start_task=ClientTask.objects.filter(status=False,is_start=False,is_approved=False,user=request.user)
        message = ""
        client_task_id = ""
        url = ""
        for i in pending_to_start_task:
            if i.notification == False:
                message = "New task added. Please check task ."
                client_task_id = i.id
                url = "/article/tasks"
        context_set={
                    'all_approved_tasks':all_approved_tasks,
                    'all_rejected_tasks':all_rejected_tasks,
                    'all_tasks':all_tasks,
                    'pending_tasks':pending_tasks,
                    "message":message,
                    "client_task_id":client_task_id,
                    "url":url
                    }
        return render(request,"article/article_dashboard.html",context_set)
    


@login_required
def index(request):
    if request.user.is_articleholder:
        current_user = request.user

        assigned_tasks = ClientTask.objects.filter(user=current_user.id).filter(is_approved=False,is_reject=False,is_rejected=False,status=False)
        # print(assigned_activities)

        context_data = {
            'tasks': assigned_tasks
        }
       
        return render(request, "article/article_index.html", context_data)

@login_required
def show_individual_task(request, task_id):
    if request.user.is_articleholder:
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
        
        # jsondata2 = json.loads(task.article_attachment_file)
        # print(jsondata2['user_id'])
        file_location = ""
        if task.article_attachment_file: 
            str_data = task.article_attachment_file.replace("'",'"')
            json_data = json.loads(str_data)
            file_location = json_data['file_location']
        context_data = {
            'task': task, 

            'client': client,
            'estimated_end_date': estimated_end_date,
            'in_time': in_time,
            'file_location':file_location,
            "estimated_time":str(int(task.task_estimated_days)  // 60) + ":" + str(int(task.task_estimated_days)  % 60)
        }
        return render(request, 'article/individual_task.html', context_data)

@login_required
def start_task(request, task_id):
    if request.user.is_articleholder:
        task = ClientTask.objects.get(id = task_id)
        
        try:
            # Update start date as current date
            task.task_start_date = date.today()

            # Update End date to Start date + estimated days
            task.task_end_date = date.today() + timedelta(days = int(task.task_estimated_date))
            task.save()
        except Exception as e:
            print(e)
        

        return HttpResponseRedirect('/article/task/{}'.format(task_id))

@login_required
def end_task(request, task_id):
    if request.user.is_articleholder:
        task = ClientTask.objects.get(id = task_id)
        
        try:
            # Update start date as current date
            task.task_end_date = date.today()
            task.save()

        except Exception as e:
            print(e)
        
        return HttpResponseRedirect('/article/task/{}'.format(task_id))

@login_required
def task_submission(request, task_id):
    if request.user.is_articleholder:
        try:
            getuser = User.objects.get(id=request.user.id)
            print(getuser)
        except User.DoesNotExist:
            getuser = "none"
        if request.method == "POST":            
            task = ClientTask.objects.get(id = task_id)
            attachment = request.FILES.get('attachment', False)
            print(attachment)
            attachment_file = FilesStorage(request,request.user,'clienttask',task.id,"task_submission",request.FILES['attachment'])
            task.article_attachment_file = attachment_file
            # if attachment:
            #     print("attachment got :")
            #     if getuser == "none":
            #         pass
            #     else:
                    # article = User.objects.get(id = request.user.id)
                    # manager = User.objects.get(id = article.linked_employee)
                    # partner = User.objects.get(id = manager.linked_employee)
                    # mainclient = User.objects.get(id = partner.linked_employee)
            #         print(article , manager , partner , mainclient)
                    
            #         try:
            #             get_max_files = MaxFiles.objects.get(main_client = mainclient.id)
            #             if int(get_max_files.current_files) == int(get_max_files.max_files):
            #                 print("error files exceeded limit")
            #             else:
            #                 path = str(settings.MEDIA_ROOT) + '\\clients\\'+ str(mainclient.username) + '\\'
            #                 directory = 'task_submission'
            #                 dire = os.path.join(path, directory)
            #                 print(dire) 

            #                 uploaded_filename = request.FILES['attachment'].name
            #                 try:
            #                     os.makedirs(dire)
            #                     print("created folder")
            #                 except:
            #                     print("folder already created")
            #                     pass
            #                 task_file_upload_path = str(dire) + '\\'+str(task_id) + '\\' + 'articleholder' +'\\'
            #                 try:
            #                     os.makedirs(task_file_upload_path)
            #                     print("created folder")
            #                 except:
            #                     print("folder already created")
            #                     pass
            #                 full_filename = os.path.join(task_file_upload_path, uploaded_filename)
            #                 fout = open(full_filename, 'wb+')
            #                 print("full_filename :",full_filename)
            #                 file_content = ContentFile( request.FILES['attachment'].read() )
            #                 # Iterate through the chunks.
            #                 for chunk in file_content.chunks():
            #                     fout.write(chunk)
            #                 fout.close()
            #                 remove_absolute_path = full_filename.replace(str(settings.MEDIA_ROOT),'')
            #                 print("removed path :",remove_absolute_path)
            #                 task.article_attachment_file =  {
            #                     "user_id":f"{request.user.id}",
            #                     "file_location":f"{remove_absolute_path}"
            #                 }
            #                 get_max_files.current_files = int(get_max_files.current_files) + 1
            #                 get_max_files.save()
            #         except MaxFiles.DoesNotExist:
            #             print("no max files found")
            # if attachment:
            #     uploaded_attachment_filename = request.FILES[u'attachment'].name
            #     uploaded_attachment_file = request.FILES['attachment']
            #     uploaded_attachment_filename = str(task_id) + "/" +  uploaded_attachment_filename
            #     # print(uploaded_attachment_filename)

            #     task.attachment_file.save(uploaded_attachment_filename, uploaded_attachment_file)
            #     # task.attachment_file = request.FILES['attachment']
            task.remark = request.POST.get('remark')
            task.status = True
            task.save()

            
        return HttpResponseRedirect('/article/task/{}'.format(task_id))

#Task Status
@login_required
def task_approval(request,task_id):
    if request.user.is_articleholder:
        task = ClientTask.objects.filter(id=task_id).update(status=True)
    return HttpResponseRedirect('/article/task/{}'.format(task_id))

@login_required
def start_working(request,task_id):
    if request.user.is_articleholder:
        task= ClientTask.objects.get(id=task_id)
        print(task)
        task.is_start=True
        task.task_start_date=date.today()
        task.is_rejected = False
        task.task_start_datetime = datetime.now()
        task.save()
        # task= ClientTask.objects.filter(id=task_id).update(is_start=True,task_start_date=date.today(),is_rejected = False)
        # print(task)
        print("yes :",datetime.now())
    return HttpResponseRedirect('/article/task/{}'.format(task_id))

@login_required
def all_task_tasks_status(request): 
    if request.user.is_articleholder:
        current_user = request.user
        approvals_tasks = ClientTask.objects.filter(user__id=current_user.id).filter(is_approved=True,status=True)
        context={

        'approvals_tasks':approvals_tasks
    }   
    return render(request,"article/approvals_tasks_status.html",context)

@login_required
def tasks_status(request):
    if request.user.is_articleholder:
        return render(request,"article/article_tasks_status.html")   

@login_required
def rejected_task_remark(request,task_id):
    if request.user.is_articleholder:
        if request.method == 'POST':
            remark_data = request.POST.get('remark')
            task = ClientTask.objects.filter(id=task_id).update(rejection_remark=remark_data)
            task_rejected = ClientTask.objects.filter(id=task_id).update(is_reject=True)
            return HttpResponseRedirect('/article/task/{}'.format(task_id))   

@login_required
def all_rejected_tasks_history(request):
    if request.user.is_articleholder:
        current_user = request.user
        rejected_tasks = ClientTask.objects.filter(user__id=current_user.id).filter(is_rejected=True)
     
        context={

        'rejected_tasks':rejected_tasks
    }  
        return render(request,"article/rejected_tasks_by_article.html",context)
        
@login_required
def tasks_pending(request):
    if request.user.is_articleholder:
        pending_tasks = ClientTask.objects.filter(user__id=request.user.id,is_start=True,status=True,is_approved=False)
        return render(request,"article/approvals_pending.html",{'pending_tasks':pending_tasks})