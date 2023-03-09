from django.shortcuts import render, HttpResponse 
from django.http.response import JsonResponse
from auditapp.models import User
from main_client.models import MaxFiles,MaxUsers,BillingDetails
from partner.models import Regulator,UserLink, Act, Activity, Industry, Task, Client,ClientTask, Entity, AuditType, ActivityAuditTypeEntity, ClientIndustryAuditTypeEntity,AuditPlanMapping
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from .serializers import ClientSerializer,BillingDetailsSerializer
# Create your views here.
from django.core.files.base import ContentFile
import os
import json
from django.conf import settings
from datetime import date, datetime ,timedelta
import xlwt
from django.contrib import messages

def FilesStorage(request,user,type_of_file_upload,task_id,file_upload_type,file):
    # print(user,task_id,file)
    removed_spaces = file.name
    removed_spaces = removed_spaces.replace(" ","_")
    uploaded_filename = removed_spaces
    if type_of_file_upload == "clienttask":
        task = ClientTask.objects.get(id = task_id)
        
        
        if request.user.is_partner:
            main_client = User.objects.get(id = user.linked_employee)
            logged_in_user = "partner"
            check_for = task.partner_attachment_file

        elif request.user.is_articleholder:
            article = User.objects.get(id = request.user.id)
            manager = User.objects.get(id = article.linked_employee)
            partner = User.objects.get(id = manager.linked_employee)
            main_client = User.objects.get(id = partner.linked_employee)
            logged_in_user = "article"
            check_for = task.article_attachment_file

        elif request.user.is_auditorclerk:
            auditor = User.objects.get(id = request.user.id)
            manager = User.objects.get(id = auditor.linked_employee)
            partner = User.objects.get(id = manager.linked_employee)
            main_client = User.objects.get(id = partner.linked_employee)
            logged_in_user = "auditor"
            check_for = task.auditor_attachment_file

        elif request.user.is_manager:
            manager = User.objects.get(id = request.user.id)
            partner = User.objects.get(id = manager.linked_employee)
            main_client = User.objects.get(id = partner.linked_employee)
            logged_in_user = "manager"
            check_for = task.manager_attachment_file
        
        get_max_files = MaxFiles.objects.get(main_client = main_client.id)
        if file_upload_type == "task_submission":
            if int(get_max_files.current_files) == int(get_max_files.max_files):
                error = "Maximum File Upload Limit Reached..!"
            else:
                path = str(settings.MEDIA_ROOT) + '/clients/'+ str(main_client.username) + '/task_submission/'+str(task_id) + '/' + logged_in_user
                # print("Path :",path)
                # dire = os.path.join(path, file_upload_type)
                # print(dire)
                try:
                    os.makedirs(path)
                    # print("file created")
                except:
                    # print("already created")
                    pass
                # task_file_upload_path = str(dire) + '/'+str(task_id) + '/' + logged_in_user 
                # try:
                #     os.makedirs(task_file_upload_path)
                # except:
                #     pass
                
                full_filename = str(path) + '/' + uploaded_filename
                print(full_filename)
                fout = open(full_filename, 'wb+')

                file_content = ContentFile( request.FILES['attachment'].read() )

                for chunk in file_content.chunks():
                    fout.write(chunk)
                fout.close()
                remove_absolute_path = full_filename.replace(str(settings.MEDIA_ROOT),'')
                print("removed path :",remove_absolute_path)
                if check_for:
                    print("file already exist hence removing old and adding new")
                    str_data = check_for.replace("'",'"')
                    print("check for")
                    json_data = json.loads(str_data)
                    file_location = json_data['file_location']
                    delete_file = str(settings.MEDIA_ROOT) + file_location
                    if os.path.exists(delete_file):
                        os.remove(delete_file)
                    print("attachment file present")
                    attachment_file =  {
                    "user_id":f"{request.user.id}",
                    "file_location":f"{remove_absolute_path}"
                    }
                else:
                    print("no previous files hence attachment added")
                    attachment_file =  {
                        "user_id":f"{request.user.id}",
                        "file_location":f"{remove_absolute_path}"
                        }
                    get_max_files.current_files = int(get_max_files.current_files) + 1
                    get_max_files.save()
                return attachment_file
    

    elif type_of_file_upload == "activity":
        if request.user.is_main_client:
            main_client = request.user
            max_files = MaxFiles.objects.get(main_client=main_client.id)
            if max_files.max_files == max_files.current_files:
                print("give error")  
                error = "Maximum number of files exceeded"
            else:
                print("save the file")
                path = str(settings.MEDIA_ROOT) + '/clients/'+ str(main_client.username) + '/activity_process_notes'
                # print("Path :",path)
                # dire = os.path.join(path, file_upload_type)
                # print(dire)
                try:
                    os.makedirs(path)
                    print("folder created")
                except:
                    print("folder already created")
                    pass
                # task_file_upload_path = str(dire) + '/'+str(task_id) + '/' + logged_in_user 
                # try:
                #     os.makedirs(task_file_upload_path)
                # except:
                #     pass
                
                full_filename = str(path) + '/' + uploaded_filename
                print(full_filename)
                fout = open(full_filename, 'wb+')

                file_content = ContentFile( request.FILES['attachment'].read() )
                for chunk in file_content.chunks():
                    fout.write(chunk)
                fout.close()
                remove_absolute_path = full_filename.replace(str(settings.MEDIA_ROOT),'')
                print("removed path :",remove_absolute_path)
                task_id.process_notes = remove_absolute_path
                task_id.save()
                max_files.current_files = int(max_files.current_files) + 1
                max_files.save()
                # path = str(settings.MEDIA_ROOT) + '/clients/'+ str(main_client.username) 
                # directory = 'activity_process_notes'
                # dire = os.path.join(path, directory)
                # print(dire) 

                # uploaded_filename = request.FILES['attachment'].name    
                # try:
                #     os.makedirs(dire)
                #     print("created folder")
                # except:
                #     print("folder already created")
                #     pass
                # full_filename = os.path.join(dire, uploaded_filename)
                # fout = open(full_filename, 'wb+')
                # print("full_filename :",full_filename)

                # file_content = ContentFile( request.FILES['attachment'].read())

                # # Iterate through the chunks.
                # for chunk in file_content.chunks():
                #     fout.write(chunk)
                # fout.close()
                # remove_absolute_path = full_filename.replace(str(settings.MEDIA_ROOT),'')
                # print("removed path :",remove_absolute_path)
                # task_id.process_notes.name = remove_absolute_path
                # # task_id.save()
                # max_files.current_files = int(max_files.current_files) + 1
                # max_files.save()
        elif request.user.is_super_admin:
            path = str(settings.MEDIA_ROOT) + '/activity_process_notes'
            # print("Path :",path)
            # dire = os.path.join(path, file_upload_type)
            # print(dire)
            try:
                os.makedirs(path)
                print("folder created")
            except:
                print("folder already created")
                pass
            # task_file_upload_path = str(dire) + '/'+str(task_id) + '/' + logged_in_user 
            # try:
            #     os.makedirs(task_file_upload_path)
            # except:
            #     pass
            
            full_filename = str(path) + '/' + uploaded_filename
            print(full_filename)
            fout = open(full_filename, 'wb+')

            file_content = ContentFile( request.FILES['attachment'].read() )
            for chunk in file_content.chunks():
                fout.write(chunk)
            fout.close()
            remove_absolute_path = full_filename.replace(str(settings.MEDIA_ROOT),'')
            print("removed path :",remove_absolute_path)
            task_id.process_notes = remove_absolute_path
            task_id.save()
            # directory = 'activity_process_notes'
            # dire = os.path.join(path, directory)

            # uploaded_filename = request.FILES['attachment'].name
            # try:
            #     os.makedirs(dire)
            #     print("created folder")
            # except:
            #     print("folder already created")
            #     pass
            # full_filename = os.path.join(dire, uploaded_filename)
            # fout = open(full_filename, 'wb+')
            # print("full_filename :",full_filename)

            # file_content = ContentFile( request.FILES['attachment'].read())

            # # Iterate through the chunks.
            # for chunk in file_content.chunks():
            #     fout.write(chunk)
            # fout.close()
            # remove_absolute_path = full_filename.replace(str(settings.MEDIA_ROOT),'')
            # print("removed path :",remove_absolute_path)
            # task_id.process_notes.name = remove_absolute_path
            # task_id.save()
    elif type_of_file_upload == "task":
        print("task is given")
        if file_upload_type == "task_update_upload":
            print("yes")
            if request.user.is_main_client:
                task = Task.objects.get(id=task_id)
                main_client = request.user
                max_files = MaxFiles.objects.get(main_client=main_client.id)
                if max_files.max_files == max_files.current_files:
                    print("give error")  
                    error = "Maximum number of files exceeded"
                else:
                    print("save the file")
                    path = str(settings.MEDIA_ROOT) + '/clients/'+ str(main_client.username) + '/task_process_notes'


                    
                    try:
                        os.makedirs(path)
                        print("created folder")
                    except:
                        print("folder already created")
                        pass
                    full_filename = str(path) + '/' + uploaded_filename
                    fout = open(full_filename, 'wb+')
                    print("full_filename :",full_filename)

                    file_content = ContentFile( request.FILES['process_notes_file'].read())

                    # Iterate through the chunks.
                    for chunk in file_content.chunks():
                        fout.write(chunk)
                    fout.close()
                    remove_absolute_path = full_filename.replace(str(settings.MEDIA_ROOT),'')
                    check_for = task.process_notes
                    if check_for:                       
                        file_location = check_for
                        print("File Location:",file_location)
                        delete_file = str(settings.MEDIA_ROOT) + file_location
                        if os.path.exists(delete_file):
                            os.remove(delete_file)
                        print("attachment file present")
                        task.process_notes = remove_absolute_path
                        task.save()
                    else:
                        
                        task.process_notes = remove_absolute_path
                        task.save()
                        max_files.current_files = int(max_files.current_files) + 1
                        max_files.save()
            elif request.user.is_super_admin:
                task = Task.objects.get(id=task_id)
               
                path = str(settings.MEDIA_ROOT) + '/task_process_notes'

 
                try:
                    os.makedirs(path)
                    print("created folder")
                except:
                    print("folder already created")
                    pass
                full_filename = str(path) + '/' + uploaded_filename
                fout = open(full_filename, 'wb+')
                print("full_filename :",full_filename)

                file_content = ContentFile( request.FILES['process_notes_file'].read())

                # Iterate through the chunks.
                for chunk in file_content.chunks():
                    fout.write(chunk)
                fout.close()
                remove_absolute_path = full_filename.replace(str(settings.MEDIA_ROOT),'')
                check_for = task.process_notes
                if check_for:                       
                    file_location = check_for
                    print("File Location:",file_location)
                    delete_file = str(settings.MEDIA_ROOT) + file_location
                    if os.path.exists(delete_file):
                        os.remove(delete_file)
                    print("attachment file present")
                    task.process_notes = remove_absolute_path
                    task.save()
                else:
                    task.process_notes = remove_absolute_path
                    task.save()
        else:
            print("no")
            if request.user.is_main_client:
                main_client = request.user
                max_files = MaxFiles.objects.get(main_client=main_client.id)
                if max_files.max_files == max_files.current_files:
                    print("give error")  
                    error = "Maximum number of files exceeded"
                else:
                    print("save the file")
                    path = str(settings.MEDIA_ROOT) + '/clients/'+ str(main_client.username) + '/task_process_notes'
   
                    try:
                        os.makedirs(path)
                        print("created folder")
                    except:
                        print("folder already created")
                        pass
                    full_filename = str(path) + '/' + uploaded_filename
                    fout = open(full_filename, 'wb+')
                    print("full_filename :",full_filename)

                    file_content = ContentFile( request.FILES['attachment'].read())

                    # Iterate through the chunks.
                    for chunk in file_content.chunks():
                        fout.write(chunk)
                    fout.close()
                    remove_absolute_path = full_filename.replace(str(settings.MEDIA_ROOT),'')
                    print("removed path :",remove_absolute_path)
                    task_id.process_notes = remove_absolute_path
                    task_id.save()
                    max_files.current_files = int(max_files.current_files) + 1
                    max_files.save()
            elif request.user.is_super_admin:
                path = str(settings.MEDIA_ROOT) + '/task_process_notes'

                try:
                    os.makedirs(path)
                    print("created folder")
                except:
                    print("folder already created")
                    pass
                full_filename = str(path) + '/' + uploaded_filename
                fout = open(full_filename, 'wb+')
                print("full_filename :",full_filename)

                file_content = ContentFile( request.FILES['attachment'].read())

                # Iterate through the chunks.
                for chunk in file_content.chunks():
                    fout.write(chunk)
                fout.close()
                remove_absolute_path = full_filename.replace(str(settings.MEDIA_ROOT),'')
                print("removed path :",remove_absolute_path)
                task_id.process_notes = remove_absolute_path
                task_id.save()



@login_required
def SuperAdminDashboard(request):
    if request.user.is_super_admin:
        print(Activity.objects.get_super_admin_activities())
        total_no_of_files = 0
        total_no_of_users = 0
        get_all_main_client = User.objects.filter(is_main_client=True)
        for i in get_all_main_client:
            max_files = MaxFiles.objects.get(main_client = i.id)
            users = User.objects.filter(linked_employee = i.id)
            for j in users:
                total_no_of_users += 1
                users_level2 = User.objects.filter(linked_employee = j.id)
                for k in users_level2:
                    total_no_of_users += 1
            total_no_of_files = total_no_of_files + int(max_files.current_files)
        print("count :",total_no_of_files , "Total no of Users :",total_no_of_users)
        
        params = {
            "no_of_clients":User.objects.filter(is_main_client=True).count(),
            "total_no_of_files":total_no_of_files,
            "total_no_of_users":total_no_of_users
        }
        return render(request,'super_admin/dashboard.html',params)

def error_404_view(request, exception):
   
    # we add the path to the the 404.html file
    # here. The name of our HTML file is 404.html
    return render(request, 'includes/404.html')

@login_required
def ShowUsers(request):
    if request.user.is_super_admin:
        if request.method == "POST":
            edit_users = request.POST.get('edit_users')
            if edit_users:
                messages.info(request, 'Your password has been changed successfully!')
                try:
                    main_client = User.objects.get(id=edit_users)
                    get_linked_employees = []
                    linked_employees = User.objects.filter(linked_employee = main_client.id)
                    for i in linked_employees:
                        get_linked_employees.append(i)
                        get_linked_employees_2 = User.objects.filter(linked_employee = i.id)
                        for j in get_linked_employees_2:
                            get_linked_employees.append(j)
                    temp = []
                    for i in get_linked_employees:
                        obj = {
                            "id":i.id,
                            "username":i.username,
                            "first_name":i.first_name,
                            "last_name":i.last_name,
                            "email":i.email
                        }
                        temp.append(obj)
                    return JsonResponse({'data':temp})
                except User.DoesNotExist:
                    pass
        user_data = []
        get_all_main_client = User.objects.filter(is_main_client=True)
        for main_client in get_all_main_client:
            partners = User.objects.filter(linked_employee = main_client.id)
            temp = []
            for partner in partners:
                temp.append(partner)
                managers = User.objects.filter(linked_employee = partner.id)
                for manager in managers:
                    temp.append(manager)
                    users = User.objects.filter(linked_employee = manager.id)
                    for user in users:
                        temp.append(user)
            obj = {
                "main_client":main_client,
                "users":temp
            }
            user_data.append(obj)

        print(user_data)
        params = {
            "users":user_data
        }
        return render(request,"super_admin/show_users.html",params)

def GetSingleUser(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                print(user)
                obj = {
                    "id":user.id,
                    "username":user.username,
                    "first_name":user.first_name,
                    "last_name":user.last_name,
                    "email":user.email
                }
                return JsonResponse({'data':obj})
            except User.DoesNotExist:
                return JsonResponse({'data':'none'})
def SaveUser(request):
    if request.method == "POST":
        user = request.POST.get("user")
        edit_username = request.POST.get("edit_username")
        edit_first_name = request.POST.get("edit_first_name")
        edit_last_name = request.POST.get("edit_last_name")
        edit_email_id = request.POST.get("edit_email_id")
        edit_password = request.POST.get("edit_password")
        if edit_username or edit_first_name or edit_last_name or edit_email_id or edit_password:
            print(user , edit_username , edit_first_name , edit_last_name , edit_email_id , edit_password)
            try:
                getuser = User.objects.get(id = user)
                if edit_username:
                    getuser.username = edit_username
                if edit_first_name:
                    getuser.first_name = edit_first_name
                if edit_last_name:
                    getuser.last_name = edit_last_name
                if edit_email_id:
                    getuser.email = edit_email_id
                if edit_password:
                    getuser.password = make_password(edit_password)
                getuser.save()

            except User.DoesNotExist:
                print("no user found")
        return JsonResponse({'data':'data'})

def DeleteUser(request):
    if request.method == "POST":
        delete_user = request.POST.get("delete_user")
        if delete_user:
            try:
                getuser = User.objects.get(id = delete_user)
                user = User.objects.get(id = getuser.linked_employee)
                if user.is_main_client:
                    max_user_creation = MaxUsers.objects.get(main_client = user.id)
                    print(max_user_creation)
                else:
                    main_client = User.objects.get(id = user.linked_employee)
                    max_user_creation = MaxUsers.objects.get(main_client = main_client.id)
                    print(max_user_creation)
                max_user_creation.current_users = int(max_user_creation.current_users) - 1
                max_user_creation.save()
                getuser.delete()


            except User.DoesNotExist:
                pass
        return JsonResponse({'data':'data'})

@login_required
def AddMainClient(request):
    if request.user.is_super_admin:
        if request.method == 'POST':
            client_first_name = request.POST.get('client_first_name')
            client_last_name = request.POST.get('client_last_name')
            client_user_name = request.POST.get('client_user_name')
            client_email_id = request.POST.get('client_email_id')
            client_mobile = request.POST.get('client_mobile')
            client_password = request.POST.get('client_password')
            client_user_creation = request.POST.get('client_user_creation')
            client_files_upload = request.POST.get('client_files_upload')
            client_billing_start_date = request.POST.get('client_billing_start_date')
            client_billing_end_date = request.POST.get('client_billing_end_date')
            if client_first_name and client_last_name and client_email_id and client_user_name and client_mobile and client_password and client_user_creation and client_files_upload:
                print(client_first_name , client_last_name , client_email_id ,client_mobile, client_user_name , client_password , client_user_creation , client_files_upload)
                print(client_billing_start_date, client_billing_end_date)
                new_user = User(
                    username=client_user_name, 
                    first_name=client_first_name, 
                    last_name=client_last_name,
                    is_main_client=True,
                    email = client_email_id,
                    mobile = client_mobile,
                    password = make_password(client_password)
                )

                new_user.save()
                get_current_user = User.objects.get(Q(username=client_user_name) & Q(email=client_email_id))
                create_maxuser = MaxUsers(
                    main_client=get_current_user.id,
                    max_users=client_user_creation,
                    current_users=0
                    )
                create_maxuser.save()
                create_maxfiles = MaxFiles(
                    main_client = get_current_user.id,
                    max_files=client_files_upload,
                    current_files = 0
                )
                create_maxfiles.save()
                print("Main Client Created with no error")
                try:
                    get_transaction_id = BillingDetails.objects.latest('id')
                    t_id = int(get_transaction_id.transactionID.replace("BAUDIT",""))
                    tid = t_id + 1
                    transactionID = str("BAUDIT") + str(tid)
                except BillingDetails.DoesNotExist:
                    transactionID = "BAUDIT1"
                create_billing_details = BillingDetails(
                    main_client = get_current_user.id,
                    start_date = client_billing_start_date,
                    end_date = client_billing_end_date,
                    current_date =  date.today(),
                    transactionID=transactionID,
                    payment_status="Realised",
                    remarks="Trial",
                    created_by = request.user.id
                )
                create_billing_details.save()
        return render(request, "super_admin/add_client.html")



@login_required
def Clients(request):
    if request.user.is_super_admin:
        if request.method == 'POST':
            billing_main_client_id = request.POST.get('billing_main_client_id')
            if billing_main_client_id:
                billing_details = BillingDetails.objects.filter(main_client = billing_main_client_id)
                if billing_details:
                    data = []
                    for i in billing_details:
                        end_date = str(i.end_date)
                        current_date = str(date.today())
                        y1,m1,d1 = current_date.split('-')
                        y2,m2,d2 = end_date.split('-')
                        date_format = "%m/%d/%Y"
                        a = datetime.strptime(f'{m1}/{d1}/{y1}', date_format)
                        b = datetime.strptime(f'{m2}/{d2}/{y2}', date_format)
                        delta = b - a
                        print (delta.days)
                        remaining_days = delta.days
                        obj = {
                            "id":i.id,
                            "main_client":i.main_client,
                            "account_type":i.account_type,
                            "bill_generation_date":i.bill_generation_date.date(),
                            "start_date":i.start_date,
                            "end_date":i.end_date,
                            "remaining_days":remaining_days,
                            "amount":i.amount,
                            "transactionID":i.transactionID,
                            "paymentmode":i.paymentmode,
                            "payment_status":i.payment_status,
                            "remarks":i.remarks
                        }
                        data.append(obj)
                    return JsonResponse({'data':data})
                else:
                    return JsonResponse({'data':'none'})
            audit_clients = request.POST.get('audit_clients')
            if audit_clients:
                client_data=[]
                all_users = User.objects.filter(linked_employee=audit_clients)
                for i in all_users:
                    get_all_clients = Client.objects.filter(assigned_partner=i.id)
                    for j in get_all_clients:
                        client_data.append(j)
                # print(client_data, len(client_data))
                client_serializer = ClientSerializer(client_data,many=True)
                return JsonResponse({'data':client_serializer.data})
            main_client_id = request.POST.get('main_client_id')
            small_user_id = request.POST.get('small_user_id')
            if main_client_id and small_user_id:
                get_small_user = User.objects.get(id = small_user_id)
                get_small_user.linked_employee = main_client_id
                get_small_user.save()
                get_max_user = MaxUsers.objects.get(main_client = main_client_id)
                if int(get_max_user.max_users) == int(get_max_user.current_users):
                    return JsonResponse({'can_add':'no'})
                else:
                    get_max_user.current_users = int(get_max_user.current_users) + 1
                    get_max_user.save()
                    return JsonResponse({'can_add':'yes'})


            edit_client_id = request.POST.get('edit_client_id')
            edit_client_first_name = request.POST.get('edit_client_first_name')
            edit_client_last_name = request.POST.get('edit_client_last_name')
            edit_client_user_name = request.POST.get('edit_client_user_name')
            edit_client_email = request.POST.get('edit_client_email')
            edit_client_password = request.POST.get('edit_client_password')
            edit_client_max_users = request.POST.get('edit_client_max_users')
            edit_client_max_files = request.POST.get('edit_client_max_files')
            if edit_client_id and (edit_client_first_name or edit_client_last_name or edit_client_user_name or edit_client_email or edit_client_password or edit_client_max_users or edit_client_max_files):
                get_user = User.objects.get(id = edit_client_id)
                if edit_client_first_name:
                    get_user.first_name = edit_client_first_name
                if edit_client_last_name:
                    get_user.last_name = edit_client_last_name
                if edit_client_user_name:
                    get_user.username = edit_client_user_name
                if edit_client_email:
                    get_user.email = edit_client_email
                if edit_client_password:
                    get_user.password = make_password(edit_client_password)
                get_user.save()
                max_users = MaxUsers.objects.get(main_client = get_user.id)
                max_files = MaxFiles.objects.get(main_client = get_user.id)
                if edit_client_max_users:
                    max_users.max_users = edit_client_max_users
                    max_users.save()
                if edit_client_max_files:
                    max_files.max_files = edit_client_max_files
                    max_files.save()
                return JsonResponse({'saved':'yes'})
                
                
                
                print(edit_client_id ,edit_client_first_name , edit_client_last_name , edit_client_user_name , edit_client_email , edit_client_password , edit_client_max_users , edit_client_max_files )
        data = []
        
        users = User.objects.filter(is_main_client=True)
        for i in users:
            count = 0
            user = User.objects.filter(linked_employee = i.id)
            for k in user:
                get_clients = Client.objects.filter(assigned_partner = k.id).count()
                count = count + get_clients
            max_users = MaxUsers.objects.get(main_client = i.id)
            max_files = MaxFiles.objects.get(main_client = i.id)
            bd = BillingDetails.objects.filter(main_client = i.id)
            if bd:
                for j in bd:
                    get_billing_details = j
                    end_date = str(j.end_date)
                    current_date = str(date.today())
                    y1,m1,d1 = current_date.split('-')
                    y2,m2,d2 = end_date.split('-')
                    date_format = "%m/%d/%Y"
                    a = datetime.strptime(f'{m1}/{d1}/{y1}', date_format)
                    b = datetime.strptime(f'{m2}/{d2}/{y2}', date_format)
                    delta = b - a
                    print (delta.days)
                    remaining_days = delta.days
            else:
                get_billing_details = ""
                remaining_days = ""
            
            
            obj = {
                "user_id":i.id,
                "first_name":i.first_name,
                "last_name":i.last_name,
                "username":i.username,
                "email":i.email,
                "max_users":max_users,
                "max_files":max_files,
                "client_count":count,
                "billing_details":get_billing_details,
                "days_remaining":remaining_days
            }
            data.append(obj)
        
        params = {
            "clients":data,
            "main_clients":User.objects.filter(is_main_client = True),
            "small_users":User.objects.filter(Q(linked_employee = None) & ~Q(is_super_admin = True) & ~Q(is_main_client = True))
        }
        return render(request, "super_admin/all_clients.html",params)

def AddBillingDetails(request):
    
    if request.method == "POST":
        billing_main_client_id = request.POST.get('billing_main_client_id')
        billing_start_date = request.POST.get('billing_start_date')
        billing_end_date = request.POST.get('billing_end_date')
        billing_account_type = request.POST.get('billing_account_type')
        billing_amount = request.POST.get('billing_amount')
        billing_payment_mode = request.POST.get('billing_payment_mode')
        billing_status = request.POST.get('billing_status')
        billing_remarks = request.POST.get('billing_remarks')
        if billing_main_client_id and billing_start_date and  billing_end_date and  billing_account_type and billing_amount and  billing_payment_mode and billing_status and billing_remarks:
            try:
                get_transaction_id = BillingDetails.objects.latest('id')
                t_id = int(get_transaction_id.transactionID.replace("BAUDIT",""))
                tid = t_id + 1
                transactionID = str("BAUDIT") + str(tid)
            except BillingDetails.DoesNotExist:
                transactionID = "BAUDIT1"
            try:
                get_previous_data = BillingDetails.objects.get(Q(main_client = billing_main_client_id) & Q(is_active = True))
                previous_data = True
            except BillingDetails.DoesNotExist:
                previous_data = False
            if previous_data == True:
                get_previous_data.is_active = False
                get_previous_data.save()
            create_billing_detail = BillingDetails(
                main_client = billing_main_client_id,
                account_type = billing_account_type,
                start_date = billing_start_date,
                end_date = billing_end_date,
                current_date=date.today(),
                amount = billing_amount,
                transactionID=transactionID,
                paymentmode = billing_payment_mode,
                payment_status = billing_status,
                created_by = request.user.id,
                remarks = billing_remarks
            )
            create_billing_detail.save()
            # print(billing_main_client_id,billing_start_date, billing_end_date, billing_account_type,billing_amount, billing_payment_mode,billing_status,billing_remarks)
        
            return JsonResponse({'saved':'yes'})
        else:
            return JsonResponse({'saved':'no'})

def MainClientReports(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        account_type = request.POST.get('account_type')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        days_remaining = request.POST.get('days_remaining')
        payment_mode = request.POST.get('payment_mode')
        # print(days_remaining)
        if username and not start_date and not end_date and not days_remaining and not account_type and not payment_mode:
            data = []
            get_clients = User.objects.filter(Q(is_main_client = True) & (Q(first_name__icontains = username) | Q(last_name__icontains = username) | Q(username__icontains = username) | Q(email__icontains = username)))
            for i in get_clients:
                get_billing_details = BillingDetails.objects.filter(main_client = i.id).latest('id')
                bill_serializer = BillingDetailsSerializer(get_billing_details,many=False)
                end_date = str(get_billing_details.end_date)
                current_date = str(date.today())
                y1,m1,d1 = current_date.split('-')
                y2,m2,d2 = end_date.split('-')
                date_format = "%m/%d/%Y"
                a = datetime.strptime(f'{m1}/{d1}/{y1}', date_format)
                b = datetime.strptime(f'{m2}/{d2}/{y2}', date_format)
                delta = b - a
                print (delta.days)
                remaining_days = delta.days
                obj = {
                    "user_id":i.id,
                    "first_name":i.first_name,
                    "last_name":i.last_name,
                    "username":i.username,
                    "email":i.email,
                    "billing_details":bill_serializer.data,
                    "remaining_days":remaining_days
                }
                data.append(obj)
            return JsonResponse({'data':data})
        elif account_type and not username and not start_date and not end_date and not days_remaining and not payment_mode:
            data = []
            get_billing_details = BillingDetails.objects.filter(Q(account_type = account_type) & Q(is_active = True))
            for i in get_billing_details:
                get_clients = User.objects.get(id = i.main_client)
                print(get_clients)
                
                # get_billing_details = BillingDetails.objects.get(Q(main_client = get_clients.id) & Q())
                bill_serializer = BillingDetailsSerializer(i,many=False)
                end_date = str(i.end_date)
                current_date = str(date.today())
                y1,m1,d1 = current_date.split('-')
                y2,m2,d2 = end_date.split('-')
                date_format = "%m/%d/%Y"
                a = datetime.strptime(f'{m1}/{d1}/{y1}', date_format)
                b = datetime.strptime(f'{m2}/{d2}/{y2}', date_format)
                delta = b - a
                print (delta.days)
                remaining_days = delta.days
                obj = {
                    "user_id":get_clients.id,
                    "first_name":get_clients.first_name,
                    "last_name":get_clients.last_name,
                    "username":get_clients.username,
                    "email":get_clients.email,
                    "billing_details":bill_serializer.data,
                    "remaining_days":remaining_days
                }
                data.append(obj)
            return JsonResponse({'data':data})
        elif start_date and end_date and not account_type and not username  and not days_remaining and not payment_mode:
            data = []
            get_billing_details = BillingDetails.objects.filter(Q(end_date__range=[start_date, end_date]) & Q(is_active = True))
            for i in get_billing_details:
                get_clients = User.objects.get(id = i.main_client)
                print(get_clients)
                
                # get_billing_details = BillingDetails.objects.get(Q(main_client = get_clients.id) & Q())
                bill_serializer = BillingDetailsSerializer(i,many=False)
                end_date = str(i.end_date)
                current_date = str(date.today())
                y1,m1,d1 = current_date.split('-')
                y2,m2,d2 = end_date.split('-')
                date_format = "%m/%d/%Y"
                a = datetime.strptime(f'{m1}/{d1}/{y1}', date_format)
                b = datetime.strptime(f'{m2}/{d2}/{y2}', date_format)
                delta = b - a
                print (delta.days)
                remaining_days = delta.days
                obj = {
                    "user_id":get_clients.id,
                    "first_name":get_clients.first_name,
                    "last_name":get_clients.last_name,
                    "username":get_clients.username,
                    "email":get_clients.email,
                    "billing_details":bill_serializer.data,
                    "remaining_days":remaining_days
                }
                data.append(obj)
            return JsonResponse({'data':data})
        elif days_remaining and not account_type and not username and not start_date and not end_date and not payment_mode:
            check_date = date.today() + timedelta(days = int(days_remaining))
            print("only remianing days :",days_remaining , "date to check :",check_date)
            data = []
            get_billing_details = BillingDetails.objects.filter(Q(end_date__lte = check_date) & Q(is_active = True))
            for i in get_billing_details:
                get_clients = User.objects.get(id = i.main_client)
                print(get_clients)
                
                # get_billing_details = BillingDetails.objects.get(Q(main_client = get_clients.id) & Q())
                bill_serializer = BillingDetailsSerializer(i,many=False)
                end_date = str(i.end_date)
                current_date = str(date.today())
                y1,m1,d1 = current_date.split('-')
                y2,m2,d2 = end_date.split('-')
                date_format = "%m/%d/%Y"
                a = datetime.strptime(f'{m1}/{d1}/{y1}', date_format)
                b = datetime.strptime(f'{m2}/{d2}/{y2}', date_format)
                delta = b - a
                print (delta.days)
                remaining_days = delta.days
                obj = {
                    "user_id":get_clients.id,
                    "first_name":get_clients.first_name,
                    "last_name":get_clients.last_name,
                    "username":get_clients.username,
                    "email":get_clients.email,
                    "billing_details":bill_serializer.data,
                    "remaining_days":remaining_days
                }
                data.append(obj)
            return JsonResponse({'data':data})
        if payment_mode and not username and not start_date and not end_date and not days_remaining and not account_type:
            print("only payment mode :",payment_mode)
            data = []
            get_billing_details = BillingDetails.objects.filter(Q(paymentmode = payment_mode) & Q(is_active = True))
            for i in get_billing_details:
                get_clients = User.objects.get(id = i.main_client)
                print(get_clients)
                
                # get_billing_details = BillingDetails.objects.get(Q(main_client = get_clients.id) & Q())
                bill_serializer = BillingDetailsSerializer(i,many=False)
                end_date = str(i.end_date)
                current_date = str(date.today())
                y1,m1,d1 = current_date.split('-')
                y2,m2,d2 = end_date.split('-')
                date_format = "%m/%d/%Y"
                a = datetime.strptime(f'{m1}/{d1}/{y1}', date_format)
                b = datetime.strptime(f'{m2}/{d2}/{y2}', date_format)
                delta = b - a
                print (delta.days)
                remaining_days = delta.days
                obj = {
                    "user_id":get_clients.id,
                    "first_name":get_clients.first_name,
                    "last_name":get_clients.last_name,
                    "username":get_clients.username,
                    "email":get_clients.email,
                    "billing_details":bill_serializer.data,
                    "remaining_days":remaining_days
                }
                data.append(obj)
            return JsonResponse({'data':data})
    return JsonResponse({'data':'data'})

@login_required
def FilesCreated(request):
    print("yes")
    if request.user.is_super_admin:
        main_client = User.objects.filter(is_main_client=True)
        data = []
       

        for i in main_client:
            path = str(settings.MEDIA_ROOT) + '\\clients\\'+ str(i.username) + '\\'
            print(path)
            count=0
            for root_dir, cur_dir, files in os.walk(path):
                count += len(files)
            obj= {
                "user_id":i.id,
                "first_name":i.first_name,
                "last_name":i.last_name,
                "username":i.username,
                "files":count
                }
            data.append(obj)
        print(data)
        
        params = {
            "data":data
        }
        return render(request, "super_admin/files_created.html",params)



def export_users_xls_superadmin(request,employee_ids):
    employees = employee_ids.split(',')
    print("employees :",employees)
    temp = []
    data = []
    for i in employees:

        get_clients = User.objects.get(id=i)
        get_billing_details = BillingDetails.objects.filter(main_client = get_clients.id).latest('id')
        print(get_billing_details)
        # bill_serializer = BillingDetailsSerializer(get_billing_details,many=False)
        end_date = str(get_billing_details.end_date)
        current_date = str(date.today())
        y1,m1,d1 = current_date.split('-')
        y2,m2,d2 = end_date.split('-')
        date_format = "%m/%d/%Y"
        a = datetime.strptime(f'{m1}/{d1}/{y1}', date_format)
        b = datetime.strptime(f'{m2}/{d2}/{y2}', date_format)
        delta = b - a
        print (delta.days)
        remaining_days = delta.days
        obj = (
            get_clients.first_name,
            get_clients.last_name,
            get_clients.username,
            get_clients.email,
            get_billing_details.account_type,
            str(get_billing_details.start_date),
            str(get_billing_details.end_date),
            remaining_days
        )
        temp.append(obj)
    print(temp)
    
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="DataSet.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Data Export') # this will make a sheet named Users Data

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['First Name', 'Last Name' , 'Email Address', 'User Name','Account Type' , 'Start Date', 'End Date' , 'Remaining Days']
    print(len(columns))
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    for row in temp:
        # print("row : ",row)
        # print("_______________________________________________________________________________________________________")
        row_num += 1
        # print(row['first_name'])
        # print(row_num)
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response

def export_pdf_superadmin(request,employee_ids):
    employees = employee_ids.split(',')
    print("employees :",employees)
    temp = []
    for i in employees:
        get_clients = User.objects.get(id=i)
        get_billing_details = BillingDetails.objects.filter(main_client = get_clients.id).latest('id')
        print(get_billing_details)
        bill_serializer = BillingDetailsSerializer(get_billing_details,many=False)
        end_date = str(get_billing_details.end_date)
        current_date = str(date.today())
        y1,m1,d1 = current_date.split('-')
        y2,m2,d2 = end_date.split('-')
        date_format = "%m/%d/%Y"
        a = datetime.strptime(f'{m1}/{d1}/{y1}', date_format)
        b = datetime.strptime(f'{m2}/{d2}/{y2}', date_format)
        delta = b - a
        print (delta.days)
        remaining_days = delta.days
        obj = {
            "user_id":get_clients.id,
            "first_name":get_clients.first_name,
            "last_name":get_clients.last_name,
            "username":get_clients.username,
            "email":get_clients.email,
            "billing_details":bill_serializer.data,
            "remaining_days":remaining_days
        }
        temp.append(obj)
    print("temp :",temp)
    params = {
        "data":temp
    }
    return render(request,"super_admin/export_pdf.html",params)

@login_required
def DatabaseMigrations(request):
    if request.user.is_super_admin:
        getallusers = User.objects.filter(~Q(is_super_admin=True) & ~Q(is_main_client=True) & ~Q(is_admin=True))
        count = 0
        for i in getallusers:
            clients = Client.objects.filter(assigned_partner = i)
            for j in clients:
                clienttask = ClientTask.objects.filter(client=j)
                for task in clienttask:
                    if task.attachment_file:
                        # print(task.attachment_file , i.id)
                        tpartner_attachment_file =  {
                            "user_id":f"{i.id}",
                            "file_location":f"{task.attachment_file}"
                        }
                        task.partner_attachment_file = tpartner_attachment_file
                        task.save()
                    if task.partner_attachment_file:
                        if type(task.partner_attachment_file) == dict:
                            pass
                        else:
                            str_data = task.partner_attachment_file.replace("'",'"')
                            try:
                                jsondata = json.loads(str_data)
                            except:
                                tpartner_attachment_file =  {
                                    "user_id":f"{i.id}",
                                    "file_location":f"{task.partner_attachment_file}"
                                }
                                task.partner_attachment_file = tpartner_attachment_file
                                task.save()
                    if task.manager_attachment_file:
                        if type(task.manager_attachment_file) == dict:
                            pass
                        else:
                            str_data = task.manager_attachment_file.replace("'",'"')
                            try:
                                jsondata = json.loads(str_data)
                            except:
                                tmanager_attachment_file =  {
                                    "user_id":f"{i.id}",
                                    "file_location":f"{task.manager_attachment_file}"
                                }
                                print(tmanager_attachment_file)
                                # print(tmanager_attachment_file)
                                task.manager_attachment_file = tmanager_attachment_file
                                task.save()
                    if task.auditor_attachment_file:
                        if type(task.auditor_attachment_file) == dict:
                            pass
                        else:
                            str_data = task.auditor_attachment_file.replace("'",'"')
                            try:
                                jsondata = json.loads(str_data)
                            except:
                                tauditor_attachment_file =  {
                                    "user_id":f"{i.id}",
                                    "file_location":f"{task.auditor_attachment_file}"
                                }
                                print(tauditor_attachment_file)
                                # print(tauditor_attachment_file)
                                task.auditor_attachment_file = tauditor_attachment_file
                                task.save()
                    if task.article_attachment_file:
                        if type(task.article_attachment_file) == dict:
                            pass
                        else:
                            str_data = task.article_attachment_file.replace("'",'"')
                            try:
                                jsondata = json.loads(str_data)
                            except:
                                tarticle_attachment_file =  {
                                    "user_id":f"{i.id}",
                                    "file_location":f"{task.article_attachment_file}"
                                }
                                print(tarticle_attachment_file)
                                # print(tarticle_attachment_file)
                                task.article_attachment_file = tarticle_attachment_file
                                task.save()
                    
        # all_clienttask = ClientTask.objects.all().count()
        # print(all_clienttask)
        print(count)
        return render(request,"super_admin/database_migrations.html")


def DashboardSuperAdmin(request):
    
    total_no_of_files = 0
    total_no_of_users = 0
    get_all_main_client = User.objects.filter(is_main_client=True)
    for i in get_all_main_client:
        max_files = MaxFiles.objects.get(main_client = i.id)
        users = User.objects.filter(linked_employee = i.id)
        for j in users:
            total_no_of_users += 1
            users_level2 = User.objects.filter(linked_employee = j.id)
            for k in users_level2:
                total_no_of_users += 1
        total_no_of_files = total_no_of_files + int(max_files.current_files)
    print("count :",total_no_of_files , "Total no of Users :",total_no_of_users)
    
    params = {
        "no_of_clients":User.objects.filter(is_main_client=True).count(),
        "total_no_of_files":total_no_of_files,
        "total_no_of_users":total_no_of_users
    }
    return JsonResponse({'data':params})





