from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from auditapp.models import User
from partner.models import Client, Act, Task
from main_client.models import MaxFiles,MaxUsers
from django.core.mail import send_mail
from partner.models import ClientTask,Industry,Entity,AuditType,ClientIndustryAuditTypeEntity
from datetime import timedelta, date , datetime
from django.db.models import Count
from django.core.files.base import ContentFile
from django.conf import settings
import os
from django.http import JsonResponse
from django.db.models import Q
import json
# Create your views here.   
@login_required
def manager_dashboard(request): 
    if request.user.is_manager:
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
        all_clients = Client.objects.filter(assigned_user=request.user).count()
        # print(all_clients)
        all_approved_tasks= ClientTask.objects.filter(client__assigned_user= request.user).filter(is_approved=True).count()
        all_rejected_tasks= ClientTask.objects.filter(client__assigned_user= request.user).filter(is_rejected=True).count()
        # approval_pending=ClientTask.objects.filter(status=True,is_start=True,is_approved=False).exclude(user = request.user)
        approval_pending = ClientTask.objects.filter(Q(status=True) & Q(is_start=True) & Q(is_approved=False) & Q(user = request.user))
        print(approval_pending)
        pending_to_start_task=ClientTask.objects.filter(status=False,is_start=False,is_approved=False,user=request.user)
        message = ""
        client_task_id = ""
        url = ""
        for i in pending_to_start_task:
            if i.notification == False:
                message = "New task added. Please check task ."
                client_task_id = i.id
                url = "/manager/tasks"

        print(pending_to_start_task)
        # for wt in approval_pending:
        #     if wt.user.is_manager:
        #         wt.remove()
        context={       
            'all_clients':all_clients,      
            'all_approved_tasks':all_approved_tasks,
            'all_rejected_tasks':all_rejected_tasks,
            'approval_pending':approval_pending.count(),
            "message":message,
            "client_task_id":client_task_id,
            "url":url
        }   
        return render(request, 'manager/manager_dashboard.html',context)


@login_required
def index(request):
    if request.user.is_manager:
        current_user = request.user

        assigned_tasks = ClientTask.objects.filter(client__assigned_user=current_user,is_approved=True)
        # print(assigned_activities)

        context_data = {
            'tasks': assigned_tasks
        }
        return render(request, "manager/manager_index.html", context_data)

@login_required
def is_rejected_tasks(request):
    if request.user.is_manager:
        current_user = request.user

        rejected_tasks = ClientTask.objects.filter(client__assigned_user=current_user,is_rejected=True)
        # print(assigned_activities)

        context_data = {
            'rejected_tasks': rejected_tasks
        }
        return render(request, "manager/rejected_task_status.html", context_data) 

@login_required
def approval_pending_tasks(request):
    if request.user.is_manager:
        waiting_approvals = []
        try:
            user = User.objects.get(id = request.user.linked_employee)
            is_main_client = True
        except User.DoesNotExist:
            is_main_client = False
        if is_main_client == True:
            print("true")
            get_users = User.objects.filter(Q(linked_employee = user.id))
            for i in get_users:
                print(i)
                client_tasks = ClientTask.objects.filter(Q(status=True) & Q(is_start=True) & Q(is_approved=False) & Q(user = i))
                for j in client_tasks:
                    waiting_approvals.append(j)
        # waiting_approvals = ClientTask.objects.filter(status=True,is_start=True,is_approved=False).exclude(user = request.user)
        print(waiting_approvals)
        # for wt in waiting_approvals:
        #     if wt.user.is_manager:
        #         wt.remove()
        context={
            'waiting_approvals':waiting_approvals
        }
        return render(request, "manager/waiting_approvals.html", context) 
@login_required 
def show_individual_task(request, task_id):
    print("yes")
    if request.user.is_manager or request.user.is_partner or request.user.is_main_client:
        task = ClientTask.objects.get(id = task_id)
        client = Client.objects.get(id = task.client_id)

        estimated_end_date = None
        in_time = False
        print(task.task_start_date)
        if task.task_start_datetime is not None and task.task_end_datetime is not None:
            estimated_end_date = task.task_start_datetime + timedelta(minutes = int(task.task_estimated_days))
            print("result 4 :",estimated_end_date , int(task.task_estimated_days))
            in_time = True
            if estimated_end_date < task.task_end_datetime:
                in_time = False
        print(in_time)
        manager_attachment_file = ""
        if task.manager_attachment_file: 
            str_data = task.manager_attachment_file.replace("'",'"')
            json_data = json.loads(str_data)
            manager_attachment_file = json_data['file_location']
        auditor_attachment_file = ""
        if task.auditor_attachment_file: 
            str_data = task.auditor_attachment_file.replace("'",'"')
            json_data = json.loads(str_data)
            auditor_attachment_file = json_data['file_location']
        article_attachment_file = ""
        if task.article_attachment_file: 
            str_data = task.article_attachment_file.replace("'",'"')
            json_data = json.loads(str_data)
            article_attachment_file = json_data['file_location']
        context_data = {
            'task': task, 
            'client': client,   
            'estimated_end_date': estimated_end_date,
            'in_time': in_time,
            "manager_attachment_file":manager_attachment_file,
            "auditor_attachment_file":auditor_attachment_file,
            "article_attachment_file":article_attachment_file,
            
            "estimated_time":str(int(task.task_estimated_days)  // 60) + ":" + str(int(task.task_estimated_days)  % 60)
        }
        return render(request, "manager/approval_files.html", context_data)

@login_required
def task_unapproved(request,task_id):
    if request.user.is_manager:
        task = ClientTask.objects.filter(id=task_id).update(status=False)
        return HttpResponseRedirect('')

@login_required
def approved_tasks(request,task_id):
    print("this page")
    if request.user.is_manager or request.user.is_partner:
        if request.user.is_manager:
            user_type = "manager"
        elif request.user.is_partner:
            user_type = "partner"
        try:
            getuser = User.objects.get(id=request.user.id)
            print(getuser)
        except User.DoesNotExist:
            getuser = "none"
        if request.method == "POST":      
            feedback = request.POST.get('feedback')      
            print(feedback)
            task = ClientTask.objects.get(id = task_id)
            task.manager_feedback = feedback

            attachment = request.FILES.get('attachment', False)
            print(attachment)
            if attachment:
                print("attachment got :")
                if getuser == "none":
                    pass
                else:
                    if user_type == "manager":
                        manager = User.objects.get(id = request.user.id)
                        partner = User.objects.get(id = manager.linked_employee)
                        mainclient = User.objects.get(id = partner.linked_employee)
                    elif user_type == "partner":
                        partner = User.objects.get(id = request.user.id)
                        mainclient = User.objects.get(id = partner.linked_employee)
                    print(mainclient)
                    try:
                        get_max_files = MaxFiles.objects.get(main_client = mainclient.id)
                        if int(get_max_files.current_files) == int(get_max_files.max_files):
                            print("error files exceeded limit")
                        else:
                            path = str(settings.MEDIA_ROOT) + '\\clients\\'+ str(mainclient.username) + '\\'
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
                            task_file_upload_path = str(dire) + '\\'+str(task_id) + '\\' + user_type +'\\'
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
                            # task.manager_attachment_file.name = remove_absolute_path
                            if request.user.is_manager:
                                task.manager_attachment_file =  {
                                    "user_id":f"{request.user.id}",
                                    "file_location":f"{remove_absolute_path}"
                                }
                            elif request.user.is_partner:
                                task.partner_attachment_file =  {
                                    "user_id":f"{request.user.id}",
                                    "file_location":f"{remove_absolute_path}"
                                }
                            get_max_files.current_files = int(get_max_files.current_files) + 1
                            get_max_files.save()
                    except MaxFiles.DoesNotExist:
                        print("no max files found")
            # if attachment:
            #     uploaded_attachment_filename = request.FILES[u'attachment'].name
            #     uploaded_attachment_file = request.FILES['attachment']
            #     uploaded_attachment_filename = str(task_id) + "/" +  uploaded_attachment_filename
            #     # print(uploaded_attachment_filename)
                
            #     task.manager_attachment_file.save(uploaded_attachment_filename, uploaded_attachment_file)
            #     # task.attachment_file = request.FILES['attachment']
            #     task.status = True
            #     task.save()

        task.is_approved = True                                                                             
        print(task)
        task.task_end_date = date.today()
        task.task_end_datetime = datetime.now()
        task.save()
        return HttpResponseRedirect(f'/manager/approval/{task_id}')
    elif request.user.is_main_client:
        task = ClientTask.objects.get(id = task_id)
        print("main client Task :",task)

@login_required
def rejected_tasks(request,task_id):
    if request.user.is_manager or request.user.is_partner:
        remark_data = request.POST.get('remark')
        task = ClientTask.objects.get(id=task_id)
        task.reject_task_remark=remark_data
        task.is_rejected = True
        task.status = False
        task.is_start = False
        task.save()
        return HttpResponseRedirect(f'/manager/approval/{task_id}')


@login_required
def manager_task(request):
    # tasks = ClientTask.objects.filter(user = None)
    # users = User.objects.exclude(is_partner=True).exclude(is_manager=True).exclude(is_admin=True)
    # context_data={
    #     'tasks': tasks,  
    #     'users': users
    # }
    return render(request,'manager/manager_task_master.html',{})

@login_required
def assign_task_to_employee(request, client_id):
    if request.method == 'POST':
        user_id = request.POST.get('user')
        task_id = request.POST.get('task_id')
        task_type = request.POST.get('task_type')
        # print(user_id)
        # print(task_id)
        task_relevance = request.POST.get('task_relevance')
        volume = request.POST.get('volume')
        samplerate = request.POST.get('samplerate')

        user = User.objects.get(pk = user_id)
        task = ClientTask.objects.get(pk = task_id)
        # print(user)
        # print(task)
        # client_id = request.POST.get('client_id') 
        # client = Client.objects.get(pk = client_id)
        try:
            # task = ClientTask(task_name=activityName, task_regulation_name=regulation, task_act_name=act, task_activity_name=activityName, client=client,user=user,task_estimated_date=estDays,task_auditing_standard=audtStnd,task_international_auditing_standard=intAudtStnd)
            # task.save()
            # print(task)
            # Deliver email to the assigned user
            task.user = user
            task.task_relevance = task_relevance
            task.task_type = task_type
            task.task_volume = volume
            task.task_sample_rate = samplerate
            task.save()
            if user.email is not None:
                
                msg = '''
                    Task Details are:=
                    Task ID: {0}
                    Task Name: {1}
                    Client: {2}
                    Auditing Standard: {3}
                    International Auditing Standard: {4}
                    Estimated Days: {5} days
                '''.format(task.id, task.task_name, task.client.client_name,
                    task.task_auditing_standard, task.task_international_auditing_standard,
                    task.task_estimated_days)
                # print(msg)
                send_mail("Task Assignment", msg, 'icraftsolution.com@gmail.com',[user.email], fail_silently=False)
        except Exception as e:
            print(e)
        return HttpResponseRedirect(f"/manager/client/{client_id}/tasks/") 

def all_task_status(request):
    if request.user.is_manager:
        client_data = request.POST.get('client')
        all_clients_data= Client.objects.filter(assigned_user_id=request.user.id)
        tasks=ClientTask.objects.filter(client_id=client_data)
        
        context={               

                  'tasks':tasks,
                  'all_clients_data':all_clients_data
                }   
        return render(request,"manager/tasks_status.html",context)

def reassign_task(request,client_id):
    # reassign_all_tasks=ClientTask.objects.all()
    if request.method=="POST":
        reassign_user = request.POST.get('user')
        task = request.POST.get('task_id')
        task = ClientTask.objects.get(id=task)  
        task.user = User.objects.get(id=reassign_user)
        task.is_reject = False
        task.save()
    return HttpResponseRedirect(f"/manager/reassign/{client_id}/tasks/")

@login_required
def assign_multiple_task(request, client_id):
    if request.method == "POST":
        user_id = request.POST.get('user')
        tasks_id = request.POST.getlist('task_id')
        # print(user_id)
        # print(tasks)
        user = User.objects.get(pk = user_id)
        for task_id in tasks_id:
            task = ClientTask.objects.get(pk = task_id)

            try:
                task.user = user
                task.save()
                if user.email is not None:
                    msg = '''
                        Task Details are:
                        Task ID: {0}
                        Task Name: {1}
                        Client: {2}
                        Auditing Standard: {3}
                        International Auditing Standard: {4}
                        Estimated Days: {5} days
                    '''.format(task.id, task.task_name, task.client.client_name,
                        task.task_auditing_standard, task.task_international_auditing_standard,
                        task.task_estimated_days)
                    # print(msg)
                    send_mail("Task Assignment", msg, 'icraftsolution.com@gmail.com',[user.email], fail_silently=False)
            except Exception as e:
                print(e)
        return HttpResponseRedirect(f"/manager/client/{client_id}/tasks/") 


def list_of_clients(request):
    if request.user.is_manager: 
        clients = Client.objects.filter(assigned_user=request.user.id)
        context = {
            "clients":clients
        }
        return render(request,"manager/list_of_clients.html",context)

def client_tasks(request,client_id):
    if request.user.is_manager:
        # print(request.user)
        client = Client.objects.get(id=client_id)
        # users = User.objects.exclude(is_partner=True).exclude(is_admin=True).exclude(is_manager=True)
        # users |= User.objects.filter(username = request.user)
        logged_in_manager = request.user.id
        users = []
        users.append(request.user)
        user = User.objects.filter(linked_employee = request.user.id)
        for i in user:
            users.append(i)

        tasks_of_client = ClientTask.objects.filter(client_id=client_id,client__assigned_user=request.user)
        reassign_tasks = ClientTask.objects.filter(client_id=client_id,is_reject=True,client__assigned_user=request.user)
        
        client_industries = ClientIndustryAuditTypeEntity.objects.values_list('industry_id',flat=True).filter(client_id=client_id).distinct()
        client_audittypes = ClientIndustryAuditTypeEntity.objects.values_list('audittype_id',flat=True).filter(client_id=client_id).distinct()
        client_entities = ClientIndustryAuditTypeEntity.objects.values_list('entity_id',flat=True).filter(client_id=client_id).distinct()
        
        industries = Industry.objects.filter(id__in=client_industries).values_list('industry_name',flat=True)
        entity = Entity.objects.filter(id__in=client_entities).values_list('entity_name',flat=True)
        audittype = AuditType.objects.filter(id__in=client_audittypes).values_list('audit_type_name',flat=True)

        context= {
            'client': client,
            'tasks': tasks_of_client,
            "users": users,
            'reassign_tasks': reassign_tasks,
            'industry': industries,
            'audittype': audittype,
            'entity' : entity,
        }

        return render(request,"manager/client_tasks.html",context)
    
def manager_tasks(request):
    if request.user.is_manager:
        current_user = request.user
        assigned_tasks = ClientTask.objects.filter(user=current_user.id).filter(is_approved=False,is_reject=False,is_rejected=False,status=False)
        # print(assigned_activities)
        context_data = {
            'tasks': assigned_tasks
        }
        return render(request, "manager/manager_tasks.html", context_data)

@login_required
def show_individual_manager_task(request, task_id):
    print("yes i am in this page")
    if request.user.is_manager:
        print("yes")
        task = ClientTask.objects.get(id = task_id)
        # seconds = estimated_days % (24 * 3600)
        # hour = seconds // 3600
        # seconds %= 3600
        # minutes = seconds // 60
        # seconds %= 60
        # print(hour,minutes)
        client = Client.objects.get(id = task.client_id)
    
        estimated_end_date = None
        in_time = False
        if task.task_start_date is not None and task.task_end_date is not None:
            estimated_end_date = task.task_start_date + timedelta(days = int(task.task_estimated_days))
            in_time = True

            if estimated_end_date < task.task_end_date:
                in_time = False
        print(in_time)
        auditor_file_location = ""
        if task.auditor_attachment_file: 
            str_data = task.auditor_attachment_file.replace("'",'"')
            json_data = json.loads(str_data)
            auditor_file_location = json_data['file_location']
        article_file_location = ""
        if task.article_attachment_file: 
            str_data = task.article_attachment_file.replace("'",'"')
            json_data = json.loads(str_data)
            article_file_location = json_data['file_location']
        manager_file_location = ""
        if task.manager_attachment_file: 
            str_data = task.manager_attachment_file.replace("'",'"')
            json_data = json.loads(str_data)
            manager_file_location = json_data['file_location']
        print(manager_file_location)
        context_data = {
            'task': task, 
            'client': client,
            "auditor_file_location":auditor_file_location,
            "article_file_location":article_file_location,
            "manager_file_location":manager_file_location,
            'estimated_end_date': estimated_end_date,
            'in_time': in_time,
            "estimated_time":str(int(task.task_estimated_days)  // 60) + ":" + str(int(task.task_estimated_days)  % 60)
        }
        return render(request, 'manager/individual_task.html', context_data)

@login_required
def start_task(request, task_id):
    if request.user.is_manager:
        task = ClientTask.objects.get(id = task_id)
        
        try:
            # Update start date as current date
            task.task_start_date = date.today()

            # Update End date to Start date + estimated days
            task.task_end_date = date.today() + timedelta(days = int(task.task_estimated_date))
            task.save()
        except Exception as e:
            print(e)
        

        return HttpResponseRedirect('/manager/task/{}'.format(task_id))

@login_required
def end_task(request, task_id):
    if request.user.is_manager:
        task = ClientTask.objects.get(id = task_id)
        
        try:
            # Update start date as current date
            task.task_end_date = date.today()
            task.save()

        except Exception as e:
            print(e)
        
        return HttpResponseRedirect('/manager/task/{}'.format(task_id))

@login_required
def manager_task_submission(request, task_id):
    if request.user.is_manager:
        try:
            getuser = User.objects.get(id=request.user.id)
            print(getuser)
        except User.DoesNotExist:
            getuser = "none"
        if request.method == "POST":            
            task = ClientTask.objects.get(id = task_id)
            print("task.id :" ,task.id)
            attachment = request.FILES.get('attachment', False)
            print("attachment :",attachment)
            if attachment:
                print("attachment got :")
                if getuser == "none":
                    pass
                else:
                    manager = User.objects.get(id = request.user.id)
                    partner = User.objects.get(id = manager.linked_employee)
                    mainclient = User.objects.get(id = partner.linked_employee)
                    print( manager , partner , mainclient)
                    try:
                        get_max_files = MaxFiles.objects.get(main_client = mainclient.id)
                        if int(get_max_files.current_files) == int(get_max_files.max_files):
                            print("error files exceeded limit")
                        else:
                            path = str(settings.MEDIA_ROOT) + '\\clients\\'+ str(mainclient.username) + '\\'
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
                            task_file_upload_path = str(dire) + '\\'+str(task_id) +  '\\' + 'manager' +'\\'
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
                            task.manager_attachment_file =  {
                                "user_id":f"{request.user.id}",
                                "file_location":f"{remove_absolute_path}"
                            }
                            get_max_files.current_files = int(get_max_files.current_files) + 1
                            get_max_files.save()
                    except MaxFiles.DoesNotExist:
                        print("no max files found")
            task.status = True
            task.is_approved = True                                                                             
            task.task_end_date = date.today()
            task.task_end_datetime = datetime.now()        
            task.remark = request.POST.get('remark')
            task.save()
                # if attachment:
                #     uploaded_attachment_filename = request.FILES[u'attachment'].name
                #     uploaded_attachment_file = request.FILES['attachment']
                #     uploaded_attachment_filename = str(task_id) + "/" +  uploaded_attachment_filename
                #     # print(uploaded_attachment_filename)

                #     task.attachment_file.save(uploaded_attachment_filename, uploaded_attachment_file)
                #     # task.attachment_file = request.FILES['attachment']
                #     task.remark = request.POST.get('remark')
                # task.status = True
                # task.save()

            
        return HttpResponseRedirect('/manager/task/{}'.format(task_id))
@login_required
def manager_start_working(request,task_id):
    print("ACCEPT KIA")
    if request.user.is_manager:
        task= ClientTask.objects.filter(id=task_id).update(is_start=True,task_start_date=date.today(),is_rejected = False,task_start_datetime = datetime.now())
    return HttpResponseRedirect('/manager/task/{}'.format(task_id))
    
@login_required
def manager_rejected_task_remark(request,task_id):
    if request.user.is_articleholder:
        if request.method == 'POST':
            remark_data = request.POST.get('remark')
            task = ClientTask.objects.filter(id=task_id).update(rejection_remark=remark_data)
            task_rejected = ClientTask.objects.filter(id=task_id).update(is_reject=True)
            return HttpResponseRedirect('/article/task/{}'.format(task_id))