import re
from django.db.models.fields import NullBooleanField
from django.template.response import TemplateResponse
from django.db.models.query import RawQuerySet
from django.shortcuts import render, HttpResponseRedirect, HttpResponse, redirect
from partner. models import Regulator,UserLink, Act, Activity, Industry, Task, Client,ClientTask, Entity, AuditType, ActivityAuditTypeEntity, ClientIndustryAuditTypeEntity,AuditPlanMapping
from auditapp.models import User
from .models import MaxUsers,MaxFiles,BillingDetails , BillingTransaction , TransactionDetails , TempTransaction
from django.core.mail import send_mail
from datetime import datetime
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.conf import settings
from django.db.models import Count
from partner.models import ClientTask, Audits,Activity_Labels
from django.db.models import Exists,Sum
from datetime import timedelta, date
from partner.models import AuditType, ClientTask
from django.contrib.auth import authenticate
import os
import json
import xlwt
from paywix.payu import Payu
from django.views.decorators.csrf import csrf_exempt
from .serializers import *
from django.core.files.base import ContentFile
from babel.numbers import format_currency
from super_admin.views import FilesStorage
# Create your views here.
@login_required
def Dashboard(request):
    if request.user.is_main_client: 
        # x,y = FilesStorage(request,request.user)
        # print(x,y)
        if request.method == 'POST':
            payment_gateway_button = request.POST.get('payment_gateway_button')
            if payment_gateway_button == "yes":
                print("payment gateway details sent")
                try:
                    get_billing_details = BillingDetails.objects.get(Q(main_client = request.user.id) & Q(is_active = True))
                    try:
                        get_temp_transaction = TempTransaction.objects.latest('id')
                        transaction_id = int(get_temp_transaction.transactionID) + 1
                        create_temp_transaction = TempTransaction(
                            main_client = request.user.id,
                            transactionID = transaction_id
                        )
                        create_temp_transaction.save()
                    except TempTransaction.DoesNotExist:
                        transaction_id = 101
                        create_temp_transaction = TempTransaction(
                            main_client = request.user.id,
                            transactionID = transaction_id
                        )
                        create_temp_transaction.save()
                    user = User.objects.get(id = request.user.id)
                    print(get_billing_details)
                    print(user)
                    payu_config = settings.PAYU_CONFIG
                    merchant_key = payu_config.get('merchant_key')
                    merchant_salt = payu_config.get('merchant_salt')
                    surl = payu_config.get('success_url')
                    furl = payu_config.get('failure_url')
                    mode = payu_config.get('mode')
                    payu = Payu(merchant_key, merchant_salt, surl, furl, mode)
                    
                    # print(payu)
                    data = {
                        'amount': 12000, 'firstname': user.first_name,
                        'email': user.email,
                        'phone': user.mobile, 'productinfo': 'test',  'lastname': user.last_name, 'address1': user.username,
                        'address2': 'test', 'city': user.username,  'state': user.username, 'country': user.username,
                        'zipcode': user.username, 'udf1': '', 'udf2': '', 'udf3': '', 'udf4': '', 'udf5': '',
                        'surl':surl,
                        'furl':furl
                    }
                    # print(data)
                    # return JsonResponse({'data':data})
                    # Make sure the transaction ID is unique
                    txnid = "OBAUDIT" + str(transaction_id)
                    data.update({"txnid": txnid})
                    payu_data = payu.transaction(**data)
                    print("Payu Data : ",payu_data)
                    return JsonResponse({'pending':'yes','amount':12000,'transactionData':payu_data,'start_date':get_billing_details.start_date,'end_date':get_billing_details.end_date})
                except BillingDetails.DoesNotExist:
                    pass
        get_expiry_days = ""
        negative_remaining_days = ""
        try:
            get_billing_details = BillingDetails.objects.get(Q(main_client = request.user.id) & Q(is_active = True))
            print(get_billing_details)
            end_date = str(get_billing_details.end_date)
            current_date = str(date.today())
            y1,m1,d1 = current_date.split('-')
            y2,m2,d2 = end_date.split('-')
            date_format = "%m/%d/%Y"
            a = datetime.strptime(f'{m1}/{d1}/{y1}', date_format)
            b = datetime.strptime(f'{m2}/{d2}/{y2}', date_format)
            delta = b - a
            remaining_days = delta.days
            print("remaining_days :",remaining_days)
            if (remaining_days <= 30 and remaining_days > -1):
                get_expiry_days = remaining_days
                print("Remaining Days :",get_expiry_days)
            elif (remaining_days <= 30 and remaining_days <= -1):
                negative_remaining_days = remaining_days * -1
                print("Days Passed",negative_remaining_days)
        except BillingDetails.DoesNotExist:
            pass
        try:
            get_max_files = MaxFiles.objects.get(main_client = request.user.id)
        except MaxFiles.DoesNotExist:
            get_max_files = ""
        all_linked_users = []
        all_partners = []
        partners = User.objects.filter(linked_employee = request.user.id)
        for partner in partners:
            all_partners.append(partner)
            all_linked_users.append(partner)
            managers = User.objects.filter(linked_employee = partner.id)
            for manager in managers:
                all_linked_users.append(manager)
                users = User.objects.filter(linked_employee = manager.id)
                for user in users:
                    all_linked_users.append(user)
        
        message = ""
        if int(get_max_files.current_files) > 0:
            print(int(get_max_files.current_files))
            current_files = int(get_max_files.current_files)
            max_files = int(get_max_files.max_files)
            percentage = (current_files / max_files) * 100
            if int(percentage) >= 80:
                message = "You have Reached 80% or more of the Maximum Files Allowed.. !"
        try:
            get_max_users = MaxUsers.objects.get(main_client = request.user.id)
            if int(get_max_users.max_users) == int(get_max_users.current_users):
                message2 = "You Have Reached Maximum User Creation..!"
            else:
                message2 = ""
        except MaxUsers.DoesNotExist:
            message2 = ""
        clients = []
        for partner in all_partners:
            get_clients = Client.objects.filter(assigned_partner=partner)
            for client in get_clients:
                clients.append(client)

        print("client count :",clients)
        params = {
            "total_users":len(all_linked_users),
            "total_files":MaxFiles.objects.get(main_client = request.user.id),
            "max_files":get_max_files,
            "message":message,
            "message2":message2,
            "bill_expire_remaining_days":get_expiry_days,
            "negative_remaining_days":negative_remaining_days,
            "client_count":len(clients)
        }
        return render(request,"main_client/dashboard.html",params)

@csrf_exempt
def paymentsuccess(request):
   
    if request.method == "POST":
        response = request.POST
        dumpdata = json.dumps(response)
        responsestring = json.loads(dumpdata)
        mihpayid = responsestring['mihpayid']
        mode = responsestring['mode']
        status = responsestring['status']
        unmappedstatus = responsestring['unmappedstatus']
        key = responsestring['key']
        txnid = responsestring['txnid']
        amount = responsestring['amount']
        cardCategory = responsestring['cardCategory']
        net_amount_debit = responsestring['net_amount_debit']
        addedon = responsestring['addedon']
        productinfo = responsestring['productinfo']
        firstname = responsestring['firstname']
        lastname = responsestring['lastname']

        email = responsestring['email']
        phone = responsestring['phone']
        payment_source = responsestring['payment_source']
        pg_TYPE = responsestring['PG_TYPE']
        bank_ref_num = responsestring['bank_ref_num']
        bankcode = responsestring['bankcode']
        cardnum = responsestring['cardnum']
        
        get_main_client = User.objects.get(Q(email = email) & Q(mobile = phone))
        add_transactiondetails = TransactionDetails(
            transactionID=txnid,
            mihpayid=mihpayid,
            mode=mode,
            status=status,
            unmappedstatus=unmappedstatus,
            key=key,
            amount=amount,
            cardCategory=cardCategory,
            net_amount_debit=net_amount_debit,
            addedon=addedon,
            productinfo=productinfo,
            firstname=firstname,
            lastname=lastname,
            email=email,
            phone=phone,
            payment_source=payment_source,
            PG_TYPE=pg_TYPE,
            bank_ref_num=bank_ref_num,
            bankcode=bankcode,
            name_on_card='',
            cardnum=cardnum)
        add_transactiondetails.save()
        get_billing_details = BillingDetails.objects.get(Q(main_client = get_main_client.id) & Q(is_active = True))
        end_date = str(get_billing_details.end_date)
        current_date = str(date.today())
        y1,m1,d1 = current_date.split('-')
        y2,m2,d2 = end_date.split('-')
        date_format = "%m/%d/%Y"
        a = datetime.strptime(f'{m1}/{d1}/{y1}', date_format)
        b = datetime.strptime(f'{m2}/{d2}/{y2}', date_format)
        delta = b - a
        print("Delta Days :",delta.days)
        remaining_days = delta.days
        if (remaining_days <= 30 and remaining_days > -1):
            get_expiry_days = remaining_days
            till_date = date.today() + timedelta(days=delta.days) + timedelta(days=180)
            add_start_date = get_billing_details.end_date + timedelta(days=1)
            print("Remaining Days :",get_expiry_days)
        elif (remaining_days <= 30 and remaining_days <= -1):
            get_expiry_days = remaining_days * -1
            till_date = date.today()  + timedelta(days=180)
            print("Days Passed",get_expiry_days)
            add_start_date = date.today()
        
        get_billing_details.is_active = False
        get_billing_details.save()
        create_new_billing_details = BillingDetails(
            main_client = get_main_client.id,
            account_type = "Purchased",
            start_date = add_start_date,
            end_date = till_date,
            current_date =  date.today(),
            amount=amount,
            transactionID=txnid,
            payment_status="Realised",
            remarks="Purchased",
            created_by = get_main_client.id
        )
        create_new_billing_details.save()
        get_latest_transaction = TempTransaction.objects.latest('id')
        get_all_except_latest_transaction = TempTransaction.objects.filter(~Q(id=get_latest_transaction.id))
        get_all_except_latest_transaction.delete()
    
        params = {
            "user":User.objects.get(id=get_main_client.id),
            "bill":BillingDetails.objects.get(Q(main_client = get_main_client.id) & Q(is_active = True))
        }
        return render(request,"main_client/payment_success.html",params)

@csrf_exempt
def paymentfailure(request):
    get_billing_details = BillingDetails.objects.get(Q(main_client = 26) & Q(is_active = True))
    end_date = str(get_billing_details.end_date)
    current_date = str(date.today())
    y1,m1,d1 = current_date.split('-')
    y2,m2,d2 = end_date.split('-')
    date_format = "%m/%d/%Y"
    a = datetime.strptime(f'{m1}/{d1}/{y1}', date_format)
    b = datetime.strptime(f'{m2}/{d2}/{y2}', date_format)
    delta = b - a
    till_date = date.today() + timedelta(days=delta.days) + timedelta(days=365)
    print(till_date)
    if request.method == "POST":
        print(request.POST)
    return render(request,"main_client/payment_failure.html")



@login_required
def AddUser(request):
    error = ""
    if request.user.is_authenticated:
        # print(request.user)
        user_id = request.user.id
    if request.method == "POST":
        fetch_data = request.POST.get('fetch_data')
        if fetch_data:
            print("Fetched data: " , fetch_data)
            if fetch_data == "manager":
                get_users = User.objects.filter(Q(linked_employee = request.user.id) & Q(is_partner = True))
                user_serializer = UserSerializer(get_users,many= True)
                return JsonResponse({'data':user_serializer.data,'link_user':'yes'})
            elif fetch_data == "auditor" or fetch_data == "article":
                partner = User.objects.filter(Q(linked_employee = request.user.id) & Q(is_partner = True))
                all_managers = []
                for i in partner:
                    get_managers = User.objects.filter(Q(linked_employee = i.id))
                    for j in get_managers:
                        all_managers.append(j)
                user_serializer = UserSerializer(all_managers,many= True)
                return JsonResponse({'data':user_serializer.data,'link_user':'yes'})
        employee_fname = request.POST.get('employee_fname')
        employee_lname = request.POST.get('employee_lname')
        employee_username = request.POST.get('employee_username')
        employee_password = request.POST.get('employee_password')
        employee_email = request.POST.get('employee_email')
        role = request.POST.get('employee_role')   
        employee_link = request.POST.get('employee_link')  
        print("Employee Link :",employee_link)   
        # print(employee_fname,employee_lname,employee_username,employee_password,employee_email,role)
        if employee_username and employee_email and employee_password and role:
            is_there = User.objects.filter(username=employee_username).exists()
            error = ""
            if is_there:
                error = "Employee exists with name: " + str(employee_username)
            else:
                new_user = None
                if role == "partner":
                    new_user = User(username=employee_username, 
                        first_name=employee_fname, 
                        last_name=employee_lname,
                        is_partner=True,
                        email = employee_email,
                        password = make_password(employee_password),
                        linked_employee=user_id
                    )
                elif role == "manager":
                    new_user = User(username=employee_username, 
                        first_name=employee_fname, 
                        last_name=employee_lname,
                        is_manager=True,
                        email = employee_email,
                        password = make_password(employee_password),
                        linked_employee=employee_link
                    )
                    
                elif role == "auditor":
                    new_user = User(username=employee_username, 
                        first_name=employee_fname, 
                        last_name=employee_lname,
                        is_auditorclerk=True,
                        email = employee_email,
                        password = make_password(employee_password),
                        linked_employee=employee_link
                    )
                elif role == "article":
                    new_user = User(username=employee_username, 
                        first_name=employee_fname, 
                        last_name=employee_lname,
                        is_articleholder=True,
                        email = employee_email,
                        password = make_password(employee_password),
                        linked_employee=employee_link
                    )
                    
                if new_user is not None:
                    add_user_count = MaxUsers.objects.get(main_client = request.user.id)
                    if add_user_count.max_users == add_user_count.current_users:
                        error = "limit of user creation exceeded. You Cannot add more users !!"
                    else:
                        print("user added successfully..!")
                        add_user_count.current_users = int(add_user_count.current_users) + 1
                        add_user_count.save()
                        new_user.save()

                    get_latest_user = User.objects.latest('id')

        userId = request.POST.get('user_id')
        newPassword = request.POST.get('new_password')
        if userId and newPassword:
            print("yes worked")
            user = User.objects.get(pk = userId)
            user.password = make_password(newPassword)
            try:
                user.save()
            except Exception as e:
                print(e)
    
    all_partner = User.objects.filter(linked_employee = user_id)

    user_lists = []
    for partner in all_partner:
        all_manager = User.objects.filter(linked_employee = partner.id)
        user_lists.append(partner)
        for manager in all_manager:
            all_others = User.objects.filter(linked_employee = manager.id)
            user_lists.append(manager)
            for others in all_others:
                user_lists.append(others)
   
    try:
        get_max_users = MaxUsers.objects.get(main_client = request.user.id)
        if int(get_max_users.max_users) == int(get_max_users.current_users):
            message2 = "You Have Reached Maximum User Creation..!"
        else:
            message2 = ""
    except MaxUsers.DoesNotExist:
        message2 = ""
    params = {
            "error": error,
            "users": user_lists,
            "message2":message2
        }
    return render(request,"main_client/add_user.html",params)

@login_required
def ShowFiles(request):
    if request.user.is_main_client:
        all_client_tasks = []
        # get_users = User.objects.filter(linked_employee = request.user.id)
        # for i in get_users:
        #     get_client_tasks = ClientTask.objects.filter(user = i)
        #     for ii in get_client_tasks:
        #         all_client_tasks.append(ii)
        #     get_users2 = User.objects.filter(linked_employee = i.id)
        #     for j in get_users2:
        #         get_client_tasks2 = ClientTask.objects.filter(user = j)
        #         for k in get_client_tasks2:
        #             all_client_tasks.append(k)
        all_tasks = []
        all_clients = Client.objects.filter(user_id = request.user.id)
        for client in all_clients:
            all_client_tasks = ClientTask.objects.filter(client = client)
            for task in all_client_tasks:
                all_tasks.append(task)
        # print(all_tasks)
        data = []
        process_notes = str(settings.MEDIA_ROOT) + '\\clients\\'+ str(request.user.username) + '\\process_notes\\' 
        activity_process_notes = str(settings.MEDIA_ROOT) + '\\clients\\'+ str(request.user.username) + '\\activity_process_notes\\' 
        process_notes_count=0
        for root_dir, cur_dir, files in os.walk(process_notes):
            process_notes_count += len(files)
        print('process notes count:', process_notes_count)
    
        activity_process_notes_count=0
        for root_dir, cur_dir, files in os.walk(activity_process_notes):
            activity_process_notes_count += len(files)
        print('activity process notes count:', activity_process_notes_count)
        for task in all_tasks:
            if task.partner_attachment_file:
                try:
                    p_json = json.loads(task.partner_attachment_file.replace("""'""",'"'))
                    partner_id = p_json['user_id']
                    data.append(partner_id)
                except:
                    pass
            if task.manager_attachment_file:
                try:
                    m_json = json.loads(task.manager_attachment_file.replace("""'""",'"'))
                    manager_id = m_json['user_id']
                    data.append(manager_id)
                except:
                    pass
            if task.auditor_attachment_file:
                try:
                    auditor_json = json.loads(task.auditor_attachment_file.replace("""'""",'"'))
                    auditor_id = auditor_json['user_id']
                    data.append(auditor_id)
                except:
                    pass
            if task.article_attachment_file:
                try:
                    article_json = json.loads(task.article_attachment_file.replace("""'""",'"'))
                    article_id = article_json['user_id']
                    data.append(article_id) 
                except:
                    pass
        student_data = [] 
        for i in data:
            user = User.objects.get(id = i)
            obj = {
                "user":user,
                "count":data.count(i)
            }
            if obj in student_data:
                pass
            else:
                # print("not found")
                student_data.append(obj)
        # print(student_data)
        
        
        params = {
            "users":student_data,
            "process_notes":process_notes_count,
            "activity_process_notes":activity_process_notes_count
        }

        

        
        

        return render(request,"main_client/show_individual_files.html",params)

@login_required
def ShowReports(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        status = request.POST.get('status')
        # priority = request.POST.get('priority')
        if user_id and not status:
            data = []
            get_user = User.objects.get(id = user_id)
            get_clients = Client.objects.filter(Q(assigned_partner = get_user) | Q(assigned_user=get_user))
            temp = []
            for i in get_clients:
                get_client_task_count = ClientTask.objects.filter(client = i).count()
                pending_tasks = ClientTask.objects.filter(is_approved_partner=False,client=i).count()
                completed_tasks = ClientTask.objects.filter(is_approved_partner=True,client=i).count()
                obj = {
                    "user_id":get_user.id,
                    "user":get_user.username,
                    "client_id":i.id,
                    "client_name":i.client_name,
                    "client_task_count":get_client_task_count,
                    "pending_task_count":pending_tasks,
                    "completed_task_count":completed_tasks
                }
                data.append(obj)
            return JsonResponse({'data':data})
        elif status and not user_id:
            users = []
            get_users = User.objects.filter(linked_employee = request.user.id)
            for i in get_users:
                users.append(i)
                get_users_2 = User.objects.filter(linked_employee = i.id)
                for j in get_users_2:
                    users.append(j)
            data = []
            for i in users:
                get_clients = Client.objects.filter(Q(assigned_partner = i) | Q(assigned_user=i))
                temp = []
                for j in get_clients:
                    if status == "pending":
                        if ClientTask.objects.filter(is_approved_partner=False,client=j):
                            print("yes")
                            get_client_task_count = ClientTask.objects.filter(client = j).count()
                            pending_tasks = ClientTask.objects.filter(is_approved_partner=False,client=j).count()
                            completed_tasks = ClientTask.objects.filter(is_approved_partner=True,client=j).count()
                            obj = {
                                "user_id":i.id,
                                "user":i.username,
                                "client_id":j.id,
                                "client_name":j.client_name,
                                "client_task_count":get_client_task_count,
                                "pending_task_count":pending_tasks,
                                "completed_task_count":completed_tasks
                            }
                            data.append(obj)
                    elif status == "completed":
                        if ClientTask.objects.filter(is_approved_partner=True,client=j):
                            print("yes")
                            get_client_task_count = ClientTask.objects.filter(client = j).count()
                            pending_tasks = ClientTask.objects.filter(is_approved_partner=False,client=j).count()
                            completed_tasks = ClientTask.objects.filter(is_approved_partner=True,client=j).count()
                            obj = {
                                "user_id":i.id,
                                "user":i.username,
                                "client_id":j.id,
                                "client_name":j.client_name,
                                "client_task_count":get_client_task_count,
                                "pending_task_count":pending_tasks,
                                "completed_task_count":completed_tasks
                            }
                            data.append(obj)
                return JsonResponse({'data':data})
        if user_id and status:
            data = []
            get_user = User.objects.get(id = user_id)
            get_clients = Client.objects.filter(Q(assigned_partner = get_user) | Q(assigned_user=get_user))
            temp = []
            for j in get_clients:
                if status == "pending":
                    if ClientTask.objects.filter(is_approved_partner=False,client=j):
                        print("yes")
                        get_client_task_count = ClientTask.objects.filter(client = j).count()
                        pending_tasks = ClientTask.objects.filter(is_approved_partner=False,client=j).count()
                        completed_tasks = ClientTask.objects.filter(is_approved_partner=True,client=j).count()
                        obj = {
                            "user_id":get_user.id,
                            "user":get_user.username,
                            "client_id":j.id,
                            "client_name":j.client_name,
                            "client_task_count":get_client_task_count,
                            "pending_task_count":pending_tasks,
                            "completed_task_count":completed_tasks
                        }
                        data.append(obj)
                elif status == "completed":
                    if ClientTask.objects.filter(is_approved_partner=True,client=j):
                        print("yes")
                        get_client_task_count = ClientTask.objects.filter(client = j).count()
                        pending_tasks = ClientTask.objects.filter(is_approved_partner=False,client=j).count()
                        completed_tasks = ClientTask.objects.filter(is_approved_partner=True,client=j).count()
                        obj = {
                            "user_id":get_user.id,
                            "user":get_user.username,
                            "client_id":j.id,
                            "client_name":j.client_name,
                            "client_task_count":get_client_task_count,
                            "pending_task_count":pending_tasks,
                            "completed_task_count":completed_tasks
                        }
                        data.append(obj)
            return JsonResponse({'data':data}) 
        
        
    return JsonResponse({'data':'data'})


def export_users_xls_mainclient(request,employee_ids):
    client_ids = employee_ids.split(',')
    temp = []
    data = []
    for i in client_ids:
        get_client = Client.objects.get(id=i)
        assigned_manager = User.objects.get(id = get_client.assigned_user.id)
        assigned_partner = User.objects.get(id=get_client.assigned_partner.id)
        get_client_task_count = ClientTask.objects.filter(client = i).count()
        pending_tasks = ClientTask.objects.filter(is_approved_partner=False,client=i).count()
        completed_tasks = ClientTask.objects.filter(is_approved_partner=True,client=i).count()
        obj = (
            # "user_id":get_user.id,
            assigned_partner.username,
            assigned_manager.username,
            get_client.id,
            get_client.client_name,
            get_client_task_count,
            pending_tasks,
            completed_tasks
        )
        data.append(obj)
    # for i in client_ids:
    #     get_client = Client.objects.get(id=i)
    #     assigned_manager = User.objects.get(id = get_client.assigned_user.id)
    #     assigned_partner = User.objects.get(id=get_client.assigned_partner.id)
    #     get_client_task_count = ClientTask.objects.filter(client = i).count()
    #     pending_tasks = ClientTask.objects.filter(is_approved_partner=False,client=i).count()
    #     completed_tasks = ClientTask.objects.filter(is_approved_partner=True,client=i).count()
    #     obj = {
    #         # "user_id":get_user.id,
    #         "assigned_partner":assigned_partner.username,
    #         "assigned_manager":assigned_manager.username,
    #         "client_id":get_client.id,
    #         "client_name":get_client.client_name,
    #         "client_task_count":get_client_task_count,
    #         "pending_task_count":pending_tasks,
    #         "completed_task_count":completed_tasks
    #     }
    #     data.append(obj)
    # return JsonResponse({'data':data})
            
    print(data)
    # return JsonResponse({'data':"data"})
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="DataSet.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Data Export') # this will make a sheet named Users Data

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Assigned Partner', 'Assigned Manager' , 'Client ID', 'Client Name','Total Client Task Count' , 'Pending Task Count', 'Completed Task Count' ]
    print(len(columns))
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    for row in data:
        # print("row : ",row)
        # print("_______________________________________________________________________________________________________")
        row_num += 1
        # print(row['first_name'])
        # print(row_num)
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response

def export_pdf_mainclient(request,employee_ids):
    employees = employee_ids.split(',')
    data = []
    for i in employees:
        get_client = Client.objects.get(id=i)
        assigned_manager = User.objects.get(id = get_client.assigned_user.id)
        assigned_partner = User.objects.get(id=get_client.assigned_partner.id)
        get_client_task_count = ClientTask.objects.filter(client = i).count()
        pending_tasks = ClientTask.objects.filter(is_approved_partner=False,client=i).count()
        completed_tasks = ClientTask.objects.filter(is_approved_partner=True,client=i).count()
        obj = {
            # "user_id":get_user.id,
            "assigned_partner":assigned_partner.username,
            "assigned_manager":assigned_manager.username,
            "client_id":get_client.id,
            "client_name":get_client.client_name,
            "client_task_count":get_client_task_count,
            "pending_task_count":pending_tasks,
            "completed_task_count":completed_tasks
        }
        data.append(obj)
    # return JsonResponse({'data':data})
    print("data :",data)
    params = {
        "data":data
    }
    return render(request,"main_client/export_pdf.html",params)

def render_client_master(request):
    if request.user.is_main_client:
        main_client_id = request.user.id
        print("Main Client Id :",main_client_id)
        clients = Client.objects.filter(user_id = request.user.id)
        industries = Industry.objects.filter(Q(user_id = request.user) | Q(is_global=True))
        audits = Audits.objects.filter(Q(user_id = request.user) | Q(is_global=True))
        entities = Entity.objects.filter(Q(user_id = request.user) | Q(is_global=True))
        audittypes = AuditType.objects.filter(Q(user_id = request.user) | Q(is_global=True))
        user = User.objects.get(id = request.user.id)
        main_client = User.objects.get(id = request.user.id)
        users = []
        all_partners = User.objects.filter(Q(is_partner = True) & Q(linked_employee = request.user.id))
        for partner in all_partners:
            all_managers = User.objects.filter(Q(is_manager = True) & Q(linked_employee = partner.id))
            for manager in all_managers:
                users.append(manager)
        ac = Client.objects.filter(user_id = request.user.id)
        # print('\n',ac)
        client_invoicing = list(AuditPlanMapping.objects.filter(client_id__in=ac).values('client_id').order_by('client_id').annotate(total_price=Sum('invoice_amount'),total_price_paid=Sum('invoice_amount_paid'),non_billable=Sum('is_billable'),ofp=Sum('out_of_pocket_expenses'),igst=Sum('igst_amount'),sgst=Sum('sgst_amount'),cgst=Sum('cgst_amount'),invoices = Count('is_billable')))
        clients_without_invoice = []
        for a in ac:
            if not AuditPlanMapping.objects.filter(client_id=a.id).exists():
                temp = {'client_id':a.id,'total_price': 0.0, 'total_price_paid': 0.0, 'non_billable': 0, 'ofp': 0.0, 'igst': 0.0, 'sgst': 0.0, 'cgst': 0.0}
                clients_without_invoice.append(temp)
        # print(clients_without_invoice)
        for c in clients_without_invoice:
            client_invoicing.append(c)
        billable_invoices = AuditPlanMapping.objects.filter(is_billable=False,client_id__in=ac).count()
        invoices_generated = AuditPlanMapping.objects.filter(invoice_number__isnull=False,client_id__in=ac).count()
        invoices_paid = AuditPlanMapping.objects.filter(invoice_number__isnull=False,client_id__in=ac,is_invoice_paid=True).count()
        invoices_not_paid = AuditPlanMapping.objects.filter(invoice_number__isnull=False,client_id__in=ac,is_invoice_paid=False).count()
        invoices_notgenerated = AuditPlanMapping.objects.filter(invoice_number__isnull=True,is_billable=True,client_id__in=ac).count()
        it = AuditPlanMapping.objects.filter(invoice_number__isnull=False,client_id__in=ac).aggregate(amount=Sum('invoice_amount'),ofp=Sum('out_of_pocket_expenses'))
        taxes = AuditPlanMapping.objects.filter(invoice_number__isnull=False,client_id__in=ac).aggregate(igst=Sum('igst_amount'),sgst=Sum('sgst_amount'),cgst=Sum('cgst_amount'))
        invoices_total = it['amount'] or 0
        ofp = it['ofp'] or 0
        igst = taxes['igst'] or 0
        sgst = taxes['sgst'] or 0
        cgst = taxes['cgst'] or 0
        addi = invoices_total+ofp+sgst+cgst+igst
        total = format_currency(addi, 'INR', locale='en_IN')
        # print(client_invoicing,'\n')

        iap = AuditPlanMapping.objects.filter(invoice_number__isnull=False,client_id__in=ac).aggregate(amount=Sum('invoice_amount_paid')) 
        invoice_amount_paid = iap['amount'] or 0
        invoice_amount_unpaid = addi - invoice_amount_paid
        iap = invoice_amount_paid
        iaup = invoice_amount_unpaid
        invoice_amount_paid = format_currency(invoice_amount_paid, 'INR', locale='en_IN')
        invoice_amount_unpaid = format_currency(invoice_amount_unpaid, 'INR', locale='en_IN')

        context_data = {
            'clients': clients,
            'industries': industries,
            'entities': entities,
            'audittypes': audittypes,
            'users' : users,
            'audits' : audits,
            'billable_invoices':billable_invoices,
            'invoices_generated':invoices_generated,
            'invoices_notgenerated':invoices_notgenerated,
            'invoices_total':total,
            'client_invoicing' : client_invoicing,
            'invoices_paid': invoices_paid,
            'invoices_not_paid': invoices_not_paid,
            'invoice_amount_paid' : invoice_amount_paid,
            'invoice_amount_unpaid' : invoice_amount_unpaid,
            'iap' : iap,
            'iaup' : iaup, 
        }
        return render(request, "master/client_master.html", context_data)
    elif request.user.is_partner:
        user = User.objects.get(id = request.user.id)
        main_client = User.objects.get(id = user.linked_employee)
        print("Main Client Id :",main_client.id)
        clients = Client.objects.filter(user_id = main_client.id)
        industries = Industry.objects.filter(user_id = main_client)
        audits = Audits.objects.filter(user_id = main_client)
        entities = Entity.objects.filter(user_id = main_client)
        audittypes = AuditType.objects.filter(user_id = main_client)
        user = User.objects.get(id = main_client.id)
        main_client = User.objects.get(id = main_client.id)
        # users = User.objects.filter((Q(is_manager = True) & Q(linked_employee = main_client.id))|(Q(is_manager = True) & Q(linked_employee = user.id)))
        linked_manager = User.objects.filter(Q(is_manager = True) & Q(linked_employee = request.user.id))
               
        
        ac = Client.objects.filter(user_id = main_client.id)
        # print('\n',ac)
        client_invoicing = list(AuditPlanMapping.objects.filter(client_id__in=ac).values('client_id').order_by('client_id').annotate(total_price=Sum('invoice_amount'),total_price_paid=Sum('invoice_amount_paid'),non_billable=Sum('is_billable'),ofp=Sum('out_of_pocket_expenses'),igst=Sum('igst_amount'),sgst=Sum('sgst_amount'),cgst=Sum('cgst_amount'),invoices = Count('is_billable')))
        clients_without_invoice = []
        for a in ac:
            if not AuditPlanMapping.objects.filter(client_id=a.id).exists():
                temp = {'client_id':a.id,'total_price': 0.0, 'total_price_paid': 0.0, 'non_billable': 0, 'ofp': 0.0, 'igst': 0.0, 'sgst': 0.0, 'cgst': 0.0}
                clients_without_invoice.append(temp)
        # print(clients_without_invoice)
        for c in clients_without_invoice:
            client_invoicing.append(c)
        billable_invoices = AuditPlanMapping.objects.filter(is_billable=False,client_id__in=ac).count()
        invoices_generated = AuditPlanMapping.objects.filter(invoice_number__isnull=False,client_id__in=ac).count()
        invoices_paid = AuditPlanMapping.objects.filter(invoice_number__isnull=False,client_id__in=ac,is_invoice_paid=True).count()
        invoices_not_paid = AuditPlanMapping.objects.filter(invoice_number__isnull=False,client_id__in=ac,is_invoice_paid=False).count()
        invoices_notgenerated = AuditPlanMapping.objects.filter(invoice_number__isnull=True,is_billable=True,client_id__in=ac).count()
        it = AuditPlanMapping.objects.filter(invoice_number__isnull=False,client_id__in=ac).aggregate(amount=Sum('invoice_amount'),ofp=Sum('out_of_pocket_expenses'))
        taxes = AuditPlanMapping.objects.filter(invoice_number__isnull=False,client_id__in=ac).aggregate(igst=Sum('igst_amount'),sgst=Sum('sgst_amount'),cgst=Sum('cgst_amount'))
        invoices_total = it['amount'] or 0
        ofp = it['ofp'] or 0
        igst = taxes['igst'] or 0
        sgst = taxes['sgst'] or 0
        cgst = taxes['cgst'] or 0
        addi = invoices_total+ofp+sgst+cgst+igst
        total = format_currency(addi, 'INR', locale='en_IN')
        # print(client_invoicing,'\n')

        iap = AuditPlanMapping.objects.filter(invoice_number__isnull=False,client_id__in=ac).aggregate(amount=Sum('invoice_amount_paid')) 
        invoice_amount_paid = iap['amount'] or 0
        invoice_amount_unpaid = addi - invoice_amount_paid
        iap = invoice_amount_paid
        iaup = invoice_amount_unpaid
        invoice_amount_paid = format_currency(invoice_amount_paid, 'INR', locale='en_IN')
        invoice_amount_unpaid = format_currency(invoice_amount_unpaid, 'INR', locale='en_IN')

        context_data = {
            'clients': clients,
            'industries': industries,
            'entities': entities,
            'audittypes': audittypes,
            'users' : linked_manager,
            'audits' : audits,
            'billable_invoices':billable_invoices,
            'invoices_generated':invoices_generated,
            'invoices_notgenerated':invoices_notgenerated,
            'invoices_total':total,
            'client_invoicing' : client_invoicing,
            'invoices_paid': invoices_paid,
            'invoices_not_paid': invoices_not_paid,
            'invoice_amount_paid' : invoice_amount_paid,
            'invoice_amount_unpaid' : invoice_amount_unpaid,
            'iap' : iap,
            'iaup' : iaup, 
        }
        return render(request, "master/client_master.html", context_data)

@login_required
def client_setup(request):
    if request.user.is_main_client:
        if request.method == "GET":
            industries = Industry.objects.filter(Q(user_id=request.user) | Q(is_global=True))
            audits = Audits.objects.filter(Q(user_id=request.user) | Q(is_global=True))
            entities = Entity.objects.filter(Q(user_id=request.user) | Q(is_global=True))
            audittypes = AuditType.objects.filter(Q(user_id=request.user) | Q(is_global=True))
            all_partner = User.objects.filter(linked_employee = request.user.id)

            partner_list = []
            manager_list = []
            for partner in all_partner:
                all_manager = User.objects.filter(linked_employee = partner.id)
                partner_list.append(partner)
                for manager in all_manager:
                    manager_list.append(manager)

        
            context_data = {
                'industries': industries,
                'entities': entities,
                'audittypes': audittypes,
                'users' : manager_list,
                'partners' : partner_list,
                'audits' : audits
            }
            return render(request, "main_client/client_setup.html", context_data)

def add_client(request):
    if request.method == 'POST':
       # print(request)
        clientName = request.POST.get('client_name')
        pan_number = request.POST.get('pan_number')
        tan_number = request.POST.get('tan_number')
        gst_number = request.POST.get('gst_number')
        assigned_partner = request.POST.get('assigned_partner')
        client_email = request.POST.get('client_email')
        finance_email = request.POST.get('finance_email')
        industries_ids = request.POST.getlist('industries')
        audit_type_ids = request.POST.getlist('audit_types')
        entities_ids = request.POST.getlist('entities')
        print("Industries :",industries_ids)
        print("Audit Type :",audit_type_ids)
        print("Entities :",entities_ids)

        partner = User.objects.get(pk = assigned_partner)
        industries = list()
        audittypes = list()
        entities = list()

        # Get the industries
        for i in industries_ids:
            industries.append(Industry.objects.get(pk=i))

        # Get the audittypes
        for i in audit_type_ids:
            audittypes.append(AuditType.objects.get(pk=i))

        # Get the entities
        for i in entities_ids:
            entities.append(Entity.objects.get(pk=i))

        client = Client(client_name = clientName, 
                client_email = client_email,
                finance_email = finance_email,
                pan_no = pan_number,
                tan_no = tan_number, 
                gst_no = gst_number,
                assigned_partner = partner,
                user_id=request.user.id)
        # print(client)
        try:
            client.save()

            activities = set()

            # Add to the mapping table
            for industry in industries:
                for audittype in audittypes:
                    for entity in entities:
                        ClientIndustryAuditTypeEntity.objects.create(
                            client = client,
                            audittype = audittype,
                            entity = entity,
                            industry = industry
                        )
                        activity_objs = ActivityAuditTypeEntity.objects.filter(audittype=audittype, entity=entity, industry=industry)
                        # print(activity_objs)
                        for activity_obj in activity_objs:
                            activities.add(activity_obj.activity_id)
            # Activities
            print(activities)
            # activities = list(activities)
            # print(activities)
            # # print(activities)
            # count = 0
            # ------------------un comment from here to create clienttask on client creation------------
            # for activity_id in activities:
            #     #activity = Activity.objects.get(pk=activity_id)
            #     tasks = Task.objects.filter(activity_id=activity_id)
            #     #act = Act.objects.filter(id=activity.act.id)
            #     # print(tasks)
            #     # area = Regulator.objects.filter(id=act.area.id)
            #     for task in tasks:
            #         activity = Activity.objects.get(id=task.activity.id)
            #         act = Act.objects.get(id=activity.act.id)
            #         ClientTask.objects.create(
            #             client=client, 
            #             task_name=task.task_name,
            #             task_estimated_days=task.task_estimated_days,
            #             task_auditing_standard=task.task_auditing_standard,
            #             task_international_auditing_standard=task.task_international_auditing_standard,
            #             activity=activity,
            #             act=act,
            #             # area_id=act.area.id
            #         )
            # --------------------------till here-------------------------
                    # count = count + 1
                    # print("Loop number :",count)


            return HttpResponseRedirect('/main_client/clients')

        except Exception as e:
            print(e)
            print("error")
        return HttpResponseRedirect('/main_client/clients')

@login_required
def add_audit_plan(request,client_id):
    print(client_id)
    if request.method == "POST":
        audit_plan_name = request.POST.get('audit_plan_name')
        audit_plan_startdate = request.POST.get('audit_plan_startdate')
        audit_plan_enddate = request.POST.get('audit_plan_enddate')
        audit_plan_actual_enddate = request.POST.get('audit_plan_actual_enddate')
        auditplan_frequency = request.POST.get('auditplan_frequency')
        auditplan_fy = request.POST.get('auditplan_fy')
        auditplan_ap = request.POST.get('auditplan_ap')
        is_billable = request.POST.get('is_billable')
        print("Data audit :",audit_plan_name , audit_plan_startdate , audit_plan_enddate , audit_plan_actual_enddate)
        if is_billable is None:
            is_billable = False
        auditplan = AuditPlanMapping(
            auditplanname=audit_plan_name, 
            start_date=audit_plan_startdate,
            estimated_end_date=audit_plan_enddate, 
            actual_end_date=audit_plan_actual_enddate,
            auditplan_frequency=auditplan_frequency, 
            finance_year=auditplan_fy,
            client_id=client_id, 
            audittype_id=auditplan_ap, 
            is_billable=is_billable
            )
        print("Saved audit :",auditplan.auditplanname ,auditplan.start_date ,auditplan.estimated_end_date ,auditplan.actual_end_date  )
        # print(audit_plan_startdate)
        try:
            auditplan.save()
            print("auditplan saved successfully :",auditplan.auditplanname ,auditplan.start_date ,auditplan.estimated_end_date ,auditplan.actual_end_date)
            auditplan = AuditPlanMapping.objects.all().last()
            industries = ClientIndustryAuditTypeEntity.objects.values_list('industry_id').filter(client_id=auditplan.client_id)
            entities = ClientIndustryAuditTypeEntity.objects.values_list('entity_id').filter(client_id=auditplan.client_id)
            # audittypes = ClientIndustryAuditTypeEntity.objects.values_list('audittype_id').filter(client_id=auditplan.client_id)
            # print(industries,entities)
            activities = set()

                # Add to the mapping table
            for industry in industries:
                    for entity in entities:
                        activity_objs = ActivityAuditTypeEntity.objects.filter(audittype=auditplan_ap, entity=entity,
                                                                            industry=industry)
                        print(activity_objs)
                        for activity_obj in activity_objs:
                            activities.add(activity_obj.activity_id)
                
            activities = list(activities)
            print(activities)
            for activity_id in activities:
                #activity = Activity.objects.get(pk=activity_id)
                tasks = Task.objects.filter(activity_id=activity_id)
                #act = Act.objects.filter(id=activity.act.id)
                print(tasks)
                # area = Regulator.objects.filter(id=act.area.id)
                for task in tasks:
                    activity = Activity.objects.get(id=task.activity.id)
                    act = Act.objects.get(id=activity.act.id)
                    ClientTask.objects.create(
                        client_id=auditplan.client_id, 
                        task_name=task.task_name,
                        task_estimated_days=task.task_estimated_days,
                        task_auditing_standard=task.task_auditing_standard,
                        task_international_auditing_standard=task.task_international_auditing_standard,
                        activity=activity,
                        act=act,
                        auditplan_id = auditplan.id          
                    )
        except Exception as e:
            raise e
        
        

    return HttpResponseRedirect(f'/main_client/client/{client_id}/profile')


def main_client_tasks(request,client_id):
    print("yup this pogae")
    if request.user.is_main_client:
        client = Client.objects.get(id=client_id)

        client_industries = ClientIndustryAuditTypeEntity.objects.values_list('industry_id',flat=True).filter(client_id=client_id).distinct()
        client_audittypes = ClientIndustryAuditTypeEntity.objects.values_list('audittype_id',flat=True).filter(client_id=client_id).distinct()
        client_entities = ClientIndustryAuditTypeEntity.objects.values_list('entity_id',flat=True).filter(client_id=client_id).distinct()
        
        industries = Industry.objects.filter(id__in=client_industries).values_list('industry_name',flat=True)
        entity = Entity.objects.filter(id__in=client_entities).values_list('entity_name',flat=True)
        audittype = AuditType.objects.filter(id__in=client_audittypes).values_list('audit_type_name',flat=True)

        print("INDUSTRY = ",client_id)

        # users = User.objects.exclude(is_admin=True).exclude(is_partner=True)
        # users |= User.objects.filter(username = request.user)
        logged_in_partner = request.user.id
        users = []
        main_client = User.objects.filter(id = request.user.id)
        for i in main_client:
            all_partners = User.objects.filter(linked_employee = i.id)
            for partner in all_partners:
                users.append(partner)
                all_managers = User.objects.filter(linked_employee = partner.id)
                for manager in all_managers:
                    users.append(manager)
                    all_others = User.objects.filter(linked_employee = manager.id)
                    for others in all_others:
                        users.append(others)
        # print(user)
        # for i in user:
        #     sub_user = User.objects.filter(linked_employee = i.id)
        #     for j in sub_user:
        #         users.append(j)
        tasks_of_client = ClientTask.objects.filter(client_id=client_id)
        reassign_tasks = ClientTask.objects.filter(client_id=client_id,is_reject=True)
        
        context= {
            'partners':User.objects.filter(Q(is_partner=True) & Q(linked_employee = request.user.id)),
            'client': client,
            'tasks': tasks_of_client,
            "users": users,
            'reassign_tasks': reassign_tasks,
            'industry': industries,
            'audittype': audittype,
            'entity' : entity,
        }

        return render(request,"main_client/client_tasks.html",context)


@login_required
def audit_plan(request, auditplan_id):
    print("yes this page :",auditplan_id)
    auditplan = AuditPlanMapping.objects.get(id=auditplan_id)
    # print("AUDIT PLANS:\n",auditplan)
    client_tasks = ClientTask.objects.filter(auditplan_id=auditplan.id)
    print(client_tasks)
    # print(client_tasks)
    labels = Activity_Labels.objects.values('activity_label_name')
    client_audittype = ClientIndustryAuditTypeEntity.objects.values_list('audittype_id').filter(client_id=auditplan.client_id).distinct()
    manager = Client.objects.values_list('assigned_user_id').filter(pk=auditplan.client_id)
    test = ClientIndustryAuditTypeEntity.objects.values('audittype_id').filter(client_id=auditplan.client_id).distinct()
    ids = []
    for r in test:
        ids.append(r['audittype_id'])
    # mng = ""
    # for m in manager:
    #     emp = User.objects.filter(pk=m[0])
    # mng = emp[0]
    # # print("=====",mng,"=====")
    ap = []
    ac = []
    for ca in ids:
        ap.append(ActivityAuditTypeEntity.objects.values_list('activity_id',flat=True).filter(audittype_id = ca).distinct())
        ac = ActivityAuditTypeEntity.objects.filter(audittype_id = ca).distinct()
    audittypes = AuditType.objects.filter(pk = auditplan.audittype_id)
    # print(ap)
    tlist = []
    j=0
    # print(len(ap))
        
    # print(ac)
    # print("client audit types")
    # print(client_tasks)
    looptimes = range(0,len(ac))
    estimated_time = 0
    client_tasks_list = []
    for task in client_tasks:
        partner_attachment_file = ""
        manager_attachment_file = ""
        auditor_attachment_file = ""
        article_attachment_file = ""
        if task.partner_attachment_file:
            str_data = task.partner_attachment_file.replace("'",'"')
            json_data = json.loads(str_data)
            partner_attachment_file = json_data['file_location']
        
        if task.manager_attachment_file:
            str_data = task.manager_attachment_file.replace("'",'"')
            json_data = json.loads(str_data)
            manager_attachment_file = json_data['file_location']
            
        if task.auditor_attachment_file:
            str_data = task.auditor_attachment_file.replace("'",'"')
            json_data = json.loads(str_data)
            auditor_attachment_file = json_data['file_location']
            
        if task.article_attachment_file:
            str_data = task.article_attachment_file.replace("'",'"')
            json_data = json.loads(str_data)
            article_attachment_file = json_data['file_location']
        
        try:
            estimated_hours = str(int(task.task_estimated_days)  // 60) + ":" + str(int(task.task_estimated_days)  % 60)
        except:
            estimated_hours = 0
        
        obj = {
            "tasks": task,
            "partner_upload":partner_attachment_file,
            "manager_upload":manager_attachment_file,
            "auditor_upload":auditor_attachment_file,
            "article_upload":article_attachment_file,
            "estimated_time":estimated_hours
            
        }
        client_tasks_list.append(obj)
    # for ct in client_tasks:
    #     print(type(ct.task_estimated_days))
        # te = int(ct.task_estimated_days)
        # estimated_time = estimated_time + te
    # print(client_tasks)
    # print(client_tasks_list)

    # print(estimated_time)
    # print("=====TIME AVAILABLE=======")
    time_available = auditplan.estimated_end_date - date.today()
    if time_available.days > 0:
        buffer = auditplan.actual_end_date - auditplan.estimated_end_date
    else:
        buffer = auditplan.actual_end_date - date.today()
    time_spent_in_days = date.today() - auditplan.start_date
    time_spend_in_hours = time_spent_in_days.days * 9
    ta = time_available.days * 9
    buff = buffer.days * 9
    # print("=======================")
    context_data = {
        'client' : auditplan.client,
        'client_tasks' : client_tasks_list,
        'client_id': auditplan.client_id,
        'labels' : labels,
        'client_audittype' : ids,
        'activity_audittype_mapping' : ac,
        'audittypes' : audittypes,
        # 'manager' : mng,
        'audit_plan' : auditplan,
        'looptimes' : looptimes,
        'time_available' : ta,
        'buffer' : buff,
        'time_spent':time_spend_in_hours
        # 'industries_activities': industries_activities
    }
    return render(request, 'main_client/audit_plan.html', context_data)

@login_required
def lock_audit_plan(request, auditplan_id):
    if request.method == "POST":
        audit_plan = AuditPlanMapping.objects.get(pk = auditplan_id)
        check = request.POST.get('lock_audit_plan')
        check_billing = request.POST.get('start_billing')
        pwd = request.POST.get('password')
        user = authenticate(username=request.user, password=pwd)
        print(check)
        print(user)
        if audit_plan is not None:
            if check == "yes" and user is not None:
                audit_plan.is_audit_plan_locked = True
                try:
                    audit_plan.save()
                    msg = "AUDIT PLAN LOCKED"
                except Exception as e:
                    print(e)
            if check_billing == "yes":
                invoice_number = request.POST.get('invoice_number')
                invoice_date = request.POST.get('invoice_date')
                invoice_amount = request.POST.get('invoice_amount')
                out_of_pocket = request.POST.get('out_of_pocket')
                audit_plan.invoice_number = invoice_number
                audit_plan.invoice_date = invoice_date
                audit_plan.invoice_amount = invoice_amount

                igst = request.POST.get('igst')
                sgst = request.POST.get('sgst')
                cgst = request.POST.get('cgst')
                
                audit_plan.igst = igst
                audit_plan.cgst = cgst
                audit_plan.sgst = sgst
                igsta = request.POST.get('igsta')
                sgsta = request.POST.get('sgsta')
                cgsta = request.POST.get('cgsta')
                audit_plan.igst_amount = igsta
                audit_plan.cgst_amount = cgsta
                audit_plan.sgst_amount = sgsta

                out_of_pocket = request.POST.get('out_of_pocket')
                ope_igst = request.POST.get('ope_igst')
                total_ope = request.POST.get('total_ope')
                audit_plan.out_of_pocket_expenses = out_of_pocket
                audit_plan.ope_igst = ope_igst

                ope_sgst = request.POST.get('ope_sgst')
                audit_plan.ope_sgst = ope_sgst

                ope_cgst = request.POST.get('ope_cgst')
                audit_plan.ope_cgst = ope_cgst
                audit_plan.total_ope = total_ope

                try:
                    audit_plan.save()
                    msg = "AUDIT PLAN LOCKED"
                except Exception as e:
                    print(e)
        return HttpResponseRedirect(f'/main_client/client/auditplan/{audit_plan.id}',{'msg' : "msg"})

@login_required
def unlock_audit_plan(request, auditplan_id):
    if request.method == "POST":
        audit_plan = AuditPlanMapping.objects.get(pk = auditplan_id)
        check = request.POST.get('unlock_audit_plan')
        pwd = request.POST.get('password')
        print("UNLOCK",check,pwd)
        user = authenticate(username=request.user, password=pwd)
        if audit_plan is not None:
            if check == "yes" and user is not None:
                audit_plan.is_audit_plan_locked = False
                try:
                    audit_plan.save()
                    msg = "AUDIT PLAN UNLOCKED"
                except Exception as e:
                    print(e)
    return HttpResponseRedirect(f'/main_client/client/auditplan/{audit_plan.id}',{'msg' : msg})



@login_required
def render_client_profile(request, client_id):
    
    if request.user.is_main_client:
        if request.method == "POST":
            get_email = request.POST.get('get_email')
            if get_email:
                try:
                    getclient = Client.objects.get(id = get_email)
                    emails = {
                        "client_email":getclient.client_email,
                        "finance_email":getclient.finance_email
                    }
                    return JsonResponse({'emails':emails})
                except Client.DoesNotExist:
                    pass
            
            send_email = request.POST.get('send_email')
            send_message = request.POST.get('send_message')
            if send_email and send_message:
                res = send_mail(
                    subject = "Client",
                    message = send_message,
                    from_email = 'icraftsolution.com@gmail.com',
                    recipient_list = [send_email],
                    fail_silently=False,
                        )
                return JsonResponse({'send':'yes'})
        area = Regulator.objects.filter(user_id = request.user)
        
        acts = Act.objects.filter(Q(user_id=request.user.id) | Q(is_global=True))
        # print("acts :",acts)
        activities = Activity.objects.filter(Q(user_id=request.user) | Q(is_global = True))
        audit_type = AuditType.objects.filter(Q(user_id=request.user) | Q(is_global = True))
        client = Client.objects.get(id = client_id)
        client_industries = ClientIndustryAuditTypeEntity.objects.values_list('industry_id',flat=True).filter(client=client).distinct()
        client_audittypes = ClientIndustryAuditTypeEntity.objects.values_list('audittype_id',flat=True).filter(client=client).distinct()
        client_entities = ClientIndustryAuditTypeEntity.objects.values_list('entity_id',flat=True).filter(client=client).distinct()
        
        industries = Industry.objects.filter(id__in=client_industries).values_list('industry_name',flat=True)
        entity = Entity.objects.filter(id__in=client_entities).values_list('entity_name',flat=True)
        audittype = AuditType.objects.filter(id__in=client_audittypes).values_list('audit_type_name',flat=True)

        audit_plan = AuditPlanMapping.objects.filter(client_id = client_id)
        
        # print(audit_plan)
        ap= AuditPlanMapping.objects.filter(client_id = client_id,is_billable=True)
        total_tasks = 0
        completed_tasks = 0
        is_pending = False
        for a in audit_plan:
            # print(a.start_date, a.estimated_end_date , a.actual_end_date)
            total_tasks = ClientTask.objects.filter(auditplan_id = a).count()
            completed_tasks = ClientTask.objects.filter(auditplan_id = a, is_approved_partner = True).count()
            pending_tasks = ClientTask.objects.filter(auditplan_id = a,is_approved=True,is_approved_partner =False).count()
            if total_tasks == completed_tasks:
                a.is_pending = True
            else:
                a.is_pending = False
            a.total_tasks = total_tasks
            a.total_pending_tasks = pending_tasks
            a.completed_tasks = completed_tasks
        # print(industries)
        # print(entity)
        # print(audittype)
        tasks_of_client = ClientTask.objects.filter(client_id=client_id)
        
        auditplans_locked = AuditPlanMapping.objects.filter(is_audit_plan_locked=True,client_id=client).count()
        auditplans_notlocked = AuditPlanMapping.objects.filter(is_audit_plan_locked=False,client_id=client).count()
        tasks_completed = ClientTask.objects.filter(is_approved_partner = True,client_id=client).count()
        tasks_notcompleted = ClientTask.objects.filter(is_approved_partner = False,client_id=client).count()

        billable_invoices = AuditPlanMapping.objects.filter(is_billable=True,client_id=client).count()
        invoices_generated = AuditPlanMapping.objects.filter(invoice_number__isnull=False,client_id=client).count()
        invoices_notgenerated = AuditPlanMapping.objects.filter(invoice_number__isnull=True,is_billable=True,client_id=client).count()
        it = AuditPlanMapping.objects.filter(invoice_number__isnull=False,client_id=client).aggregate(amount=Sum('invoice_amount'),ofp=Sum('out_of_pocket_expenses'))
        taxes = AuditPlanMapping.objects.filter(invoice_number__isnull=False,client_id=client).aggregate(igst=Sum('igst_amount'),sgst=Sum('sgst_amount'),cgst=Sum('cgst_amount'))
        invoices_total = it['amount'] or 0
        ofp = it['ofp'] or 0
        igst = taxes['igst'] or 0
        sgst = taxes['sgst'] or 0
        cgst = taxes['cgst'] or 0
        addi = invoices_total+ofp+sgst+cgst+igst
        total = format_currency(addi, 'INR', locale='en_IN')
        # print(tasks_completed , total_tasks , round((float(tasks_completed) / (float(total_tasks) )) * 100,2))
        context_data = {
            'client': client,
            'tasks': tasks_of_client,
            'acts': acts,
            'activities': activities,
            'industry': industries,
            'audittype': audittype,
            'entity' : entity,
            'audit_plans' : audit_plan,
            'invoices' : ap,
            'allap' : audit_type,
            'billable_invoices':billable_invoices,
            'invoices_generated':invoices_generated,
            'invoices_notgenerated':invoices_notgenerated,
            'invoices_total':total,
            'locked_ap' : auditplans_locked,
            'unlocked_ap' : auditplans_notlocked,
            'tasks_completed' : tasks_completed,
            'tasks_notcompleted':tasks_notcompleted
        }

        return render(request, 'main_client/client_profile.html', context_data)
    elif request.user.is_partner:
        main_client = User.objects.get(id = request.user.linked_employee)
        
        area = Regulator.objects.filter(user_id = main_client)
        acts = []
        for i in area:
            act = Act.objects.filter(area = i)
            acts.append(act)
        # print("acts :",acts)
        activities = Activity.objects.filter(user_id=main_client)
        audit_type = AuditType.objects.filter(user_id=main_client)
        client = Client.objects.get(id = client_id)
        client_industries = ClientIndustryAuditTypeEntity.objects.values_list('industry_id',flat=True).filter(client=client).distinct()
        client_audittypes = ClientIndustryAuditTypeEntity.objects.values_list('audittype_id',flat=True).filter(client=client).distinct()
        client_entities = ClientIndustryAuditTypeEntity.objects.values_list('entity_id',flat=True).filter(client=client).distinct()
        
        industries = Industry.objects.filter(id__in=client_industries).values_list('industry_name',flat=True)
        entity = Entity.objects.filter(id__in=client_entities).values_list('entity_name',flat=True)
        audittype = AuditType.objects.filter(id__in=client_audittypes).values_list('audit_type_name',flat=True)

        audit_plan = AuditPlanMapping.objects.filter(client_id = client_id)
        
        # print(audit_plan)
        ap= AuditPlanMapping.objects.filter(client_id = client_id,is_billable=True)
        total_tasks = 0
        completed_tasks = 0
        is_pending = False
        for a in audit_plan:
            print(a.start_date, a.estimated_end_date , a.actual_end_date)
            total_tasks = ClientTask.objects.filter(auditplan_id = a).count()
            completed_tasks = ClientTask.objects.filter(auditplan_id = a, is_approved_partner = True).count()
            pending_tasks = ClientTask.objects.filter(auditplan_id = a,is_approved=True,is_approved_partner =False).count()
            if total_tasks == completed_tasks:
                a.is_pending = True
            else:
                a.is_pending = False
            a.total_tasks = total_tasks
            a.total_pending_tasks = pending_tasks
            a.completed_tasks = completed_tasks
        # print(industries)
        # print(entity)
        # print(audittype)
        tasks_of_client = ClientTask.objects.filter(client_id=client_id)
        
        auditplans_locked = AuditPlanMapping.objects.filter(is_audit_plan_locked=True,client_id=client).count()
        auditplans_notlocked = AuditPlanMapping.objects.filter(is_audit_plan_locked=False,client_id=client).count()
        tasks_completed = ClientTask.objects.filter(is_approved_partner = True,client_id=client).count()
        tasks_notcompleted = ClientTask.objects.filter(is_approved_partner = False,client_id=client).count()

        billable_invoices = AuditPlanMapping.objects.filter(is_billable=True,client_id=client).count()
        invoices_generated = AuditPlanMapping.objects.filter(invoice_number__isnull=False,client_id=client).count()
        invoices_notgenerated = AuditPlanMapping.objects.filter(invoice_number__isnull=True,is_billable=True,client_id=client).count()
        it = AuditPlanMapping.objects.filter(invoice_number__isnull=False,client_id=client).aggregate(amount=Sum('invoice_amount'),ofp=Sum('out_of_pocket_expenses'))
        taxes = AuditPlanMapping.objects.filter(invoice_number__isnull=False,client_id=client).aggregate(igst=Sum('igst_amount'),sgst=Sum('sgst_amount'),cgst=Sum('cgst_amount'))
        invoices_total = it['amount'] or 0
        ofp = it['ofp'] or 0
        igst = taxes['igst'] or 0
        sgst = taxes['sgst'] or 0
        cgst = taxes['cgst'] or 0
        addi = invoices_total+ofp+sgst+cgst+igst
        total = format_currency(addi, 'INR', locale='en_IN')
        # print(tasks_completed , total_tasks , round((float(tasks_completed) / (float(total_tasks) )) * 100,2))
        context_data = {
            'client': client,
            'tasks': tasks_of_client,
            'acts': acts,
            'activities': activities,
            'industry': industries,
            'audittype': audittype,
            'entity' : entity,
            'audit_plans' : audit_plan,
            'invoices' : ap,
            'allap' : audit_type,
            'billable_invoices':billable_invoices,
            'invoices_generated':invoices_generated,
            'invoices_notgenerated':invoices_notgenerated,
            'invoices_total':total,
            'locked_ap' : auditplans_locked,
            'unlocked_ap' : auditplans_notlocked,
            'tasks_completed' : tasks_completed,
            'tasks_notcompleted':tasks_notcompleted
        }

        return render(request, 'main_client/client_profile.html', context_data)
# --------------------------------Masters--------------------------------
@login_required
def render_areas_master(request):
    if request.user.is_super_admin:
        areas = Regulator.objects.filter(Q(is_global=True))
        audittypes=Audits.objects.filter(Q(is_global=True))

        my_areas = Regulator.objects.filter(Q(is_global=True))
        non_global_areas = Regulator.objects.filter(Q(is_global=False))
    else:
        areas = Regulator.objects.filter(Q(user_id=request.user.id) | Q(is_global=True))
        audittypes=Audits.objects.filter(Q(user_id=request.user.id) | Q(is_global=True))

        my_areas = Regulator.objects.filter(Q(user_id=request.user.id) & Q(is_global=False))
        non_global_areas = []
    # Pass it to the template
    context_data = {
        'areas': areas,
        "audittypes" : audittypes,
        "my_areas":my_areas,
        "non_global_areas":non_global_areas
    }
    
    return render(request, "master/areas_master.html",context_data)
        

@login_required
def area_make_global(request,area_id):
    print(area_id)
    area = Regulator.objects.get(id = area_id)
    area.is_global = True
    area.save()
    return HttpResponseRedirect("/main_client/areas")
# ----------------------------------Regulators -------------------------------------
@login_required
def add_area(request):
    if request.method == "POST":
        area_name = request.POST.get('area_name')
        type_of_audit = request.POST.get('types_of_audits')
        is_there = Regulator.objects.filter((Q(area_name=area_name) & Q(user_id=request.user.id)) | (Q(is_global=True) & Q(area_name=area_name))).exists()
        # print(is_there)
        print(is_there)
        error = ""
        if is_there:
            error = "Regulator exists with name: " + str(area_name)
        else:
            if request.user.is_super_admin:
                new_area = Regulator(user=request.user,area_name=area_name,type_of_audits=type_of_audit,is_global=True)
            else:
                new_area = Regulator(user=request.user,area_name=area_name,type_of_audits=type_of_audit,is_global=False)
            new_area.save()
            return HttpResponseRedirect('/main_client/areas')
        
        if request.user.is_super_admin:
            areas = Regulator.objects.filter(Q(is_global=True))
            audittypes=Audits.objects.filter(Q(is_global=True))

            my_areas = Regulator.objects.filter(Q(is_global=True))
            non_global_areas = Regulator.objects.filter(Q(is_global=False))
        else:
            areas = Regulator.objects.filter(Q(user_id=request.user.id) | Q(is_global=True))
            audittypes=Audits.objects.filter(Q(user_id=request.user.id) | Q(is_global=True))

            my_areas = Regulator.objects.filter(Q(user_id=request.user.id) & Q(is_global=False))
        non_global_areas = []
        context_data = {
            "error": error,
            'areas': areas,
            "audittypes" : audittypes,
            "my_areas":my_areas,
            "non_global_areas":non_global_areas
        }
        return render(request, "master/areas_master.html",context_data)
    else:
        return redirect('render_areas_master')
@login_required
def remove_area(request, area_id):
    
    if area_id:
        area = Regulator.objects.get(pk = area_id)
        area.delete()
        return HttpResponseRedirect("/main_client/areas")  

@login_required
def edit_area(request):

    if request.method == 'POST':
        areaId = request.POST.get('edit_area_id')
        areaName = request.POST.get('edit_area_name')
        type_of_audit = request.POST.get('edit_types_of_audits')
        area = Regulator.objects.get(pk = areaId)
        area.area_name = areaName
        area.type_of_audits = type_of_audit
        area.save()
        return HttpResponseRedirect("/main_client/areas")

@login_required
def render_activity_label_master(request):
    if request.method == 'GET':
        if request.user.is_super_admin:
            activity_label = Activity_Labels.objects.filter(Q(is_global=True))
            my_activity_label = Activity_Labels.objects.filter(Q(is_global=True))
            non_global_activity_labels = Activity_Labels.objects.filter(Q(is_global=False))
        else:
            activity_label = Activity_Labels.objects.filter(Q(user_id=request.user.id) | Q(is_global=True))
            my_activity_label = Activity_Labels.objects.filter(Q(user_id=request.user.id) & Q(is_global=False))
            non_global_activity_labels = []
        context_data = {
            'activity_label': activity_label,
            'my_activity_label': my_activity_label,
            'non_global_activity_labels':non_global_activity_labels
        }
        return render(request, "master/activity_label_master.html",context_data)

@login_required
def activity_label_make_global(request,activitylabel_id):
    print(activitylabel_id)
    activitylabel = Activity_Labels.objects.get(id = activitylabel_id)
    activitylabel.is_global = True
    activitylabel.save()
    return HttpResponseRedirect("/main_client/activitylabel")

@login_required
def add_activitylabel(request):
    if request.method == 'POST':
        activity_label_name = request.POST.get('activity_label_name')
        
        is_there = Activity_Labels.objects.filter((Q(activity_label_name=activity_label_name) & Q(user_id=request.user.id)) | (Q(is_global=True) & Q(activity_label_name=activity_label_name))).exists()
        
        error = ""
        if is_there:
            error = "Activity Label exists with name: " + str(activity_label_name)
        else:
            if request.user.is_super_admin:
                new_activity_label = Activity_Labels(user=request.user,activity_label_name=activity_label_name,is_global=True)
            else:
                new_activity_label = Activity_Labels(user=request.user,activity_label_name=activity_label_name)
            try:
                new_activity_label.save()
                return HttpResponseRedirect('/main_client/activitylabel')
            except Exception as e:
                print(e)
        if request.user.is_super_admin:
            activity_label = Activity_Labels.objects.filter(Q(is_global=True))
            my_activity_label = Activity_Labels.objects.filter(Q(is_global=True))
            non_global_activity_labels = Activity_Labels.objects.filter(Q(is_global=False))
        else:
            activity_label = Activity_Labels.objects.filter(Q(user_id=request.user.id) | Q(is_global=True))
            my_activity_label = Activity_Labels.objects.filter(Q(user_id=request.user.id) & Q(is_global=False))
            non_global_activity_labels = []
        context_data = {
            "error":error,
            'activity_label': activity_label,
            'my_activity_label': my_activity_label,
            'non_global_activity_labels':non_global_activity_labels
        }
        return render(request, "master/activity_label_master.html",context_data)  
    else:
        return redirect('render_activity_label_master')

@login_required
def edit_activitylabel(request):
    if request.method == 'POST':
        edit_activity_label_id = request.POST.get('edit_activity_label_id')
        edit_activity_label_name = request.POST.get('edit_activity_label_name')


        acticity_label = Activity_Labels.objects.get(pk=edit_activity_label_id)
        acticity_label.activity_label_name = edit_activity_label_name
        # print(industry)
        try:
            acticity_label.save()
        except Exception as e:
            print(e)
        return HttpResponseRedirect("/main_client/activitylabel")

@login_required
def remove_activitylabel(request, activitylabel_id):
    if activitylabel_id:
        activity_label = Activity_Labels.objects.get(pk = activitylabel_id)
        activity_label.delete()
        return HttpResponseRedirect("/main_client/activitylabel") 

# -----------------------------------Acts-----------------------------------------
@login_required
def render_acts_master(request):

    # Get all the acts and areas from the master tables
    if request.user.is_super_admin:
        acts = Act.objects.filter(Q(is_global = True))
        areas = Regulator.objects.filter(Q(is_global=True))
        my_acts = Act.objects.filter(Q(is_global = True))
        my_areas = Regulator.objects.filter(Q(is_global=True))
        non_global_areas = Act.objects.filter(Q(is_global=False))
    else:
        acts = Act.objects.filter(Q(user_id=request.user.id) | Q(is_global=True))
        areas = Regulator.objects.filter(Q(user_id=request.user.id) | Q(is_global=True))
        my_acts = Act.objects.filter(Q(user_id=request.user.id) | Q(is_global=False))
        my_areas = Regulator.objects.filter(Q(user_id=request.user.id) & Q(is_global=False))
        non_global_areas = []
    # Pass it to the template
    context_data = {
        'acts': acts,
        'areas': areas,
        'my_acts': my_acts,
        'my_areas': my_areas,
        'non_global_areas':non_global_areas
    }
    return render(request, 'master/acts_master.html', context_data)


@login_required
def acts_make_global(request,act_id):
    print(act_id)
    acts = Act.objects.get(id = act_id)
    acts.is_global = True
    acts.save()
    return HttpResponseRedirect("/main_client/acts")

@login_required
def add_act(request):
    if request.method == 'POST':
        #  Get the values from the template
        act_name = request.POST.get('act_name')
        area = request.POST.get('area')

        # Get the area
        area = Regulator.objects.get(id = area)

        # Check if the act exists
        is_there = Act.objects.filter((Q(act_name=act_name) & Q(user_id = request.user.id)) | (Q(is_global=True) & Q(act_name=act_name))).exists()
        
        error = ""
        if is_there:
            error = "Act exists with name: " + str(act_name)
        else:
            # Create a new act
            if request.user.is_super_admin:
                new_act = Act(user=request.user,act_name=act_name, area=area,is_global=True)
            else:
                new_act = Act(user=request.user,act_name=act_name, area=area)
            try:
                # Save it to database
                new_act.save()
                return HttpResponseRedirect('/main_client/acts')
            except Exception as e:
                raise e
        if request.user.is_super_admin:
            acts = Act.objects.filter(Q(is_global = True))
            areas = Regulator.objects.filter(Q(is_global=True))
            my_acts = Act.objects.filter(Q(is_global = True))
            my_areas = Regulator.objects.filter(Q(is_global=True))
            non_global_areas = Act.objects.filter(Q(is_global=False))
        else:
            acts = Act.objects.filter(Q(user_id=request.user.id) | Q(is_global=True))
            areas = Regulator.objects.filter(Q(user_id=request.user.id) | Q(is_global=True))
            my_acts = Act.objects.filter(Q(user_id=request.user.id) & Q(is_global=False))
            my_areas = Regulator.objects.filter(Q(user_id=request.user.id) & Q(is_global=False))
            non_global_areas = []
        # Pass it to the template
        context_data = {
            "error":error,
            'acts': acts,
            'areas': areas,
            'my_acts': my_acts,
            'my_areas': my_areas,
            'non_global_areas':non_global_areas
        }
        return render(request, "master/acts_master.html", context_data) 
    else:
        return redirect('render_acts_master')
@login_required
def get_industries(request):
    if request.method == "POST":
        act_id = request.POST.get('act_id')
        # print(audittype_id)
        industries = Act.objects.get(pk=act_id).industry.all()
        print(industries)
        data = []
        for industry in industries:
            data.append(industry.id)
        return JsonResponse({'industries' : data})

@login_required
def edit_act(request):
    if request.method == 'POST':
        # Get all the values from template
        actId = request.POST.get('edit_act_id')
        actName = request.POST.get('edit_act_name')
        area = request.POST.get('edit_area')
            
        # Get the act from master
        act = Act.objects.get(pk = actId)

        # Get the area from master
        area = Regulator.objects.get(pk = area)

        # Rename the act
        act.act_name = actName
        act.area = area
        try:
            # Save it to database
            act.save()
        except Exception as e:
            print(e)
        
        return HttpResponseRedirect("/main_client/acts") 

@login_required
def remove_act(request, act_id):
    if act_id:
        # Get the object from master
        act = Act.objects.get(pk = act_id)

        # Delete it from master
        act.delete()
        return HttpResponseRedirect("/main_client/acts") 
# ---------------------------------------------------End Acts----------------------------------
# ------------------------------------------------Audit Type-----------------------------------

@login_required
def render_audittype_master(request):
    if request.method == 'GET':
        # Get all the records from master
        
        if request.user.is_super_admin:
            audittypes = AuditType.objects.filter(Q(is_global=True))
            my_audittypes = AuditType.objects.filter(Q(is_global=True))
            non_global_audit_type = AuditType.objects.filter(Q(is_global=False))
        else:
            audittypes = AuditType.objects.filter(Q(user_id = request.user.id) | Q(is_global=True))
            my_audittypes = AuditType.objects.filter(Q(user_id = request.user.id) & Q(is_global=False))
            non_global_audit_type = []
        # Pass it to template
        context_data = {
            'audittypes': audittypes,
            'my_audittypes': my_audittypes,
            'non_global_audit_type':non_global_audit_type
        }
        return render(request, "master/audittype_master.html",context_data)

@login_required
def audit_type_make_global(request,audittype_id):
    print(audittype_id)
    audit_type = AuditType.objects.get(id = audittype_id)
    audit_type.is_global = True
    audit_type.save()
    return HttpResponseRedirect("/main_client/audittypes")

@login_required
def add_audittype(request):
    if request.method == "POST":
        # Get the form values from template
        audittype_name = request.POST.get('audit_type_name')
        
        # Check if already exists
        is_there = AuditType.objects.filter((Q(audit_type_name=audittype_name) & Q(user_id=request.user.id)) | (Q(audit_type_name=audittype_name) & Q(is_global=True))).exists()
        
        error = ""
        if is_there:
            error = "Audit Type exists with name: " + str(audittype_name)
        else:
            # Create a new Audit type
            if request.user.is_super_admin:
                new_audittype = AuditType(user=request.user,audit_type_name=audittype_name,is_global=True)
            else:
                new_audittype = AuditType(user=request.user,audit_type_name=audittype_name)
            try:
                # Save it to DB
                new_audittype.save()
                return HttpResponseRedirect('/main_client/audittypes')
            except Exception as e:
                print(e)

        if request.user.is_super_admin:
            audittypes = AuditType.objects.filter(Q(is_global=True))
            my_audittypes = AuditType.objects.filter(Q(is_global=True))
            non_global_audit_type = AuditType.objects.filter(Q(is_global=False))
        else:
            audittypes = AuditType.objects.filter(Q(user_id = request.user.id) | Q(is_global=True))
            my_audittypes = AuditType.objects.filter(Q(user_id = request.user.id) & Q(is_global=False))
            non_global_audit_type = []
        # Pass it to template
        context_data = {
            "error":error,
            'audittypes': audittypes,
            'my_audittypes': my_audittypes,
            'non_global_audit_type':non_global_audit_type
        }
        return render(request, "master/audittype_master.html",context_data)  
    else:
        return redirect('render_audittype_master')

@login_required
def edit_audittype(request):
    if request.method == 'POST':
        # Get the values from the form
        audittypeId = request.POST.get('edit_audittype_id')
        audittypeName = request.POST.get('edit_audittype_name')

        # Get the audit type from master
        audittype = AuditType.objects.get(pk=audittypeId)

        # Rename the audit type
        audittype.audit_type_name = audittypeName
        
        try:
            # Save it to DB
            audittype.save()
        except Exception as e:
            print(e)
        return HttpResponseRedirect("/main_client/audittypes")

@login_required
def remove_audittype(request, audittype_id):
    if audittype_id:
        # Get the audit type from DB
        audittype = AuditType.objects.get(pk = audittype_id)

        # Delete the audit type
        audittype.delete()
        return HttpResponseRedirect("/main_client/audittypes") 

# ----------------------------------------End Audit Type -------------------------------

@login_required
def render_industry_master(request):
    if request.method == 'GET':
        if request.user.is_super_admin:
            industries = Industry.objects.filter(Q(is_global=True))
            my_industries = Industry.objects.filter(Q(is_global=True))
            non_global_industry = Industry.objects.filter(is_global=False)
        else:
            industries = Industry.objects.filter(Q(user_id = request.user.id) | Q(is_global=True))
            my_industries = Industry.objects.filter(Q(user_id = request.user.id) & Q(is_global=False))
            non_global_industry = []
        context_data = {
            'industries': industries,
            'my_industries': my_industries,
            'non_global_industry':non_global_industry
            
        }
        return render(request, "master/industry_master.html",context_data)
@login_required
def industry_make_global(request,industry_id):
    print(industry_id)
    industry = Industry.objects.get(id = industry_id)
    industry.is_global = True
    industry.save()
    return HttpResponseRedirect("/main_client/industries")


@login_required
def add_industry(request):
    if request.method == 'POST':
        industry_name = request.POST.get('industry_name')
        
        is_there = Industry.objects.filter((Q(industry_name=industry_name) & Q(user_id=request.user.id)) | (Q(industry_name=industry_name) & Q(is_global=True))).exists()
        
        error = ""
        if is_there:
            error = "Industry exists with name: " + str(industry_name)
        else:
            if request.user.is_super_admin:
                new_industry = Industry(user=request.user,industry_name=industry_name,is_global=True)
            else:
                new_industry = Industry(user=request.user,industry_name=industry_name)
            try:
                new_industry.save()
                return HttpResponseRedirect('/main_client/industries')
            except Exception as e:
                print(e)

        if request.user.is_super_admin:
            industries = Industry.objects.filter(Q(is_global=True))
            my_industries = Industry.objects.filter(Q(is_global=True))
            non_global_industry = Industry.objects.filter(is_global=False)
        else:
            industries = Industry.objects.filter(Q(user_id = request.user.id) | Q(is_global=True))
            my_industries = Industry.objects.filter(Q(user_id = request.user.id) & Q(is_global=False))
            non_global_industry = []
        context_data = {
            "error":error,
            'industries': industries,
            'my_industries': my_industries,
            'non_global_industry':non_global_industry
            
        }
        return render(request, "master/industry_master.html",context_data)  
    else:
        return redirect('render_industry_master')

@login_required
def edit_industry(request):
    if request.method == 'POST':
        industryId = request.POST.get('edit_industry_id')
        industryName = request.POST.get('edit_industry_name')


        industry = Industry.objects.get(pk=industryId)
        industry.industry_name = industryName
        # print(industry)
        try:
            industry.save()
        except Exception as e:
            print(e)
        return HttpResponseRedirect("/main_client/industries")

@login_required
def remove_industry(request, industry_id):
    if industry_id:
        industry = Industry.objects.get(pk = industry_id)
        industry.delete()
        return HttpResponseRedirect("/main_client/industries") 
# -----------------------------------End Industry--------------------------------

@login_required
def render_audits_master(request):
    if request.method == 'GET':
        if request.user.is_super_admin:
            audits = Audits.objects.filter(Q(is_global=True))
            my_audits = Audits.objects.filter(Q(is_global=True))
            non_global_audits = Audits.objects.filter(Q(is_global=False))
        else:
            audits = Audits.objects.filter(Q(user_id = request.user.id) | Q(is_global=True))
            my_audits = Audits.objects.filter(Q(user_id = request.user.id) & Q(is_global=False))
            non_global_audits = []
        context_data = {
            'audits': audits,
            'my_audits': my_audits,
            'non_global_audits':non_global_audits
        }
        return render(request, "master/audits_master.html",context_data)




@login_required
def audits_make_global(request,audit_id):
    print(audit_id)
    audit = Audits.objects.get(id = audit_id)
    audit.is_global = True
    audit.save()
    return HttpResponseRedirect("/main_client/audits")

@login_required
def add_audits(request):
    if request.method == 'POST':
        audit_name = request.POST.get('audit_name')
        
        is_there = Audits.objects.filter((Q(audit_name=audit_name) & Q(user_id = request.user.id)) | (Q(is_global=True) & Q(audit_name=audit_name))).exists()
        print(is_there)
        error = ""
        if is_there:
            error = "Audit exists with name: " + str(audit_name)
        else:
            if request.user.is_super_admin:
                new_audit = Audits(user=request.user,audit_name=audit_name,is_global=True)
            else:
                new_audit = Audits(user=request.user,audit_name=audit_name,is_global=False)
            try:
                new_audit.save()
                return HttpResponseRedirect('/main_client/audits')
            except Exception as e:
                print(e)
        print(error)
        if request.user.is_super_admin:
            audits = Audits.objects.filter(Q(is_global=True))
            my_audits = Audits.objects.filter(Q(is_global=True))
            non_global_audits = Audits.objects.filter(Q(is_global=False))
        else:
            audits = Audits.objects.filter(Q(user_id = request.user.id) | Q(is_global=True))
            my_audits = Audits.objects.filter(Q(user_id = request.user.id) & Q(is_global=False))
            non_global_audits = []
        context_data = {
            "error":error,
            'audits': audits,
            'my_audits': my_audits,
            'non_global_audits':non_global_audits
        }
        
        return render(request, "master/audits_master.html",context_data)  
    else:
        return redirect('render_audits_master')
@login_required
def edit_audits(request):
    if request.method == 'POST':
        edit_audits_id = request.POST.get('edit_audits_id')
        edit_audits_name = request.POST.get('edit_audits_name')


        audit = Audits.objects.get(pk=edit_audits_id)
        audit.audit_name = edit_audits_name
        # print(audit)
        try:
            audit.save()
        except Exception as e:
            print(e)
        return HttpResponseRedirect("/main_client/audits")

@login_required
def remove_audit(request, audit_id):
    if audit_id:
        audit = Audits.objects.get(pk = audit_id)
        audit.delete()
        return HttpResponseRedirect("/main_client/audits") 


# ---------------------------------------------------Activities--------------------------------

@login_required
def render_activity_master(request):
    # current_partner = User.objects.get(id = request.user.id)
    main_client = request.user
    path = str(settings.MEDIA_ROOT) + '\\clients\\'+ str(main_client.username) + '\\'
    count=0
    for root_dir, cur_dir, files in os.walk(path):
        count += len(files)
    print('file count:', count)
    if request.method == "GET":
        if request.user.is_super_admin:
            activities = Activity.objects.filter(Q(is_global = True))
            audit_types = AuditType.objects.filter(Q(is_global = True))
            entities = Entity.objects.filter(Q(is_global = True))
            industries = Industry.objects.filter(Q(is_global = True))
            area = Regulator.objects.filter(Q(is_global = True))
            acts = Act.objects.filter(Q(is_global = True))
            
            label = Activity_Labels.objects.filter(Q(is_global = True))

            my_activities = Activity.objects.filter(Q(is_global = True))
            non_global_activity = Activity.objects.filter(Q(is_global = False))
        else:
            activities = Activity.objects.filter(Q(user_id = request.user) | Q(is_global = True))
            audit_types = AuditType.objects.filter(Q(user_id = request.user) | Q(is_global = True))
            entities = Entity.objects.filter(Q(user_id = request.user) | Q(is_global = True))
            industries = Industry.objects.filter(Q(user_id = request.user) | Q(is_global = True))
            area = Regulator.objects.filter(Q(user_id = request.user) | Q(is_global = True))
            acts = Act.objects.filter(Q(user_id = request.user) | Q(is_global = True))
            
            label = Activity_Labels.objects.filter(Q(user_id = request.user) | Q(is_global = True))

            my_activities = Activity.objects.filter(Q(user_id = request.user) & Q(is_global = False))
            non_global_activity = []
        context_data = {
            'activities': activities,
            'audittypes': audit_types,
            'entities': entities,
            'industries': industries,
            'acts': acts,
            'label' : label,
            'my_activities':my_activities,
            'non_global_activity':non_global_activity
        }
    
        return render(request, "master/activity_master.html",context_data)

@login_required
def activity_make_global(request,activity_id):
    print(activity_id)
    activity = Activity.objects.get(id = activity_id)
    activity.is_global = True
    activity.save()
    return HttpResponseRedirect("/main_client/activities")


@login_required
def add_activity(request):
    if request.method == "POST":

        activity_name = request.POST.get('activity_name')
        activity_description = request.POST.get('activity_description')
        act = request.POST.get('act')
        label = request.POST.get('label')
        audit_type_ids = request.POST.getlist('audittype')
        entities_ids = request.POST.getlist('entities')
        industries_ids = request.POST.getlist('industries')
        print("Add Activity : ",activity_name , activity_description , act , label , audit_type_ids , entities_ids,industries_ids)
        industries = list()
        audittypes = list()
        entities = list()

        # Get the industries
        for i in industries_ids:
            industries.append(Industry.objects.get(pk=i))

        # Get the audittypes
        for i in audit_type_ids:
            audittypes.append(AuditType.objects.get(pk=i))

        # Get the entities
        for i in entities_ids:
            entities.append(Entity.objects.get(pk=i))


        is_there = Activity.objects.filter((Q(activity_name=activity_name) & Q(user_id = request.user.id)) | (Q(activity_name=activity_name) & Q(is_global=True))).exists()
        print("is there ",is_there)
        error = ""
        if is_there:
            error = "Activity exists with name: " + str(activity_name)
        else:
            if request.user.is_super_admin:
                activity = Activity(user=request.user,activity_name=activity_name, 
                    activity_description = activity_description,
                    act = Act.objects.get(pk=act),
                    label = Activity_Labels.objects.get(pk=label),is_global=True)
            else:
                activity = Activity(user=request.user,activity_name=activity_name, 
                    activity_description = activity_description,
                    act = Act.objects.get(pk=act),
                    label = Activity_Labels.objects.get(pk=label))

            
            try:
                activity.save()
                
                for industry in industries:
                    for audittype in audittypes:
                        for entity in entities:
                            ActivityAuditTypeEntity.objects.create(
                                activity = activity,
                                audittype = audittype,
                                entity = entity,
                                industry = industry
                            )
                # return HttpResponseRedirect('/main_client/activities')
            except Exception as e:
                raise e
        # activity_id = Activity.objects.get(activity_name = activity_name)
        activity = Activity.objects.get(activity_name = activity_name)
        # print(activity_id)
        
        attachment = request.FILES.get('attachment', False)
        # print(attachment)
        if is_there == False:
            if attachment:
                attachment_file = FilesStorage(request,request.user,"activity",activity,"activity_task_submission",request.FILES['attachment'])
                # activity.partner_attachment_file = attachment_file
                # main_client = User.objects.get(id = request.user.id)
                # max_files = MaxFiles.objects.get(main_client=main_client.id)
                # if max_files.max_files == max_files.current_files:
                #     print("give error")  
                #     error = "Maximum number of files exceeded"
                # else:
                #     print("save the file")
                #     path = str(settings.MEDIA_ROOT) + '\\clients\\'+ str(main_client.username) + '\\'
                #     directory = 'process_notes'
                #     dire = os.path.join(path, directory)
                #     print(dire) 

                #     uploaded_filename = request.FILES['attachment'].name    
                #     try:
                #         os.makedirs(dire)
                #         print("created folder")
                #     except:
                #         print("folder already created")
                #         pass
                #     full_filename = os.path.join(dire, uploaded_filename)
                #     fout = open(full_filename, 'wb+')
                #     print("full_filename :",full_filename)
                #     file_content = ContentFile( request.FILES['attachment'].read() )

                #     # Iterate through the chunks.
                #     for chunk in file_content.chunks():
                #         fout.write(chunk)
                #     fout.close()
                #     remove_absolute_path = full_filename.replace(str(settings.MEDIA_ROOT),'')
                #     print("removed path :",remove_absolute_path)
                #     activity.process_notes.name = remove_absolute_path
                #     # uploaded_attachment_filename = request.FILES[u'attachment'].name
                #     # uploaded_attachment_file = request.FILES['attachment']
                #     # uploaded_attachment_filename = str(activity_id) + "/" +  uploaded_attachment_filename
                #     # activity.process_notes.save(uploaded_attachment_filename, uploaded_attachment_file)
                    
                #     # Add to the mapping table
                #     activity.save()
                #     max_files.current_files = int(max_files.current_files) + 1
                #     max_files.save()
        if request.user.is_super_admin:
            activities = Activity.objects.filter(Q(is_global = True))
            audit_types = AuditType.objects.filter(Q(is_global = True))
            entities = Entity.objects.filter(Q(is_global = True))
            industries = Industry.objects.filter(Q(is_global = True))
            area = Regulator.objects.filter(Q(is_global = True))
            acts = Act.objects.filter(Q(is_global = True))
            
            label = Activity_Labels.objects.filter(Q(is_global = True))

            my_activities = Activity.objects.filter(Q(is_global = True))
            non_global_activity = Activity.objects.filter(Q(is_global = False))
        else:
            activities = Activity.objects.filter(Q(user_id = request.user) | Q(is_global = True))
            audit_types = AuditType.objects.filter(Q(user_id = request.user) | Q(is_global = True))
            entities = Entity.objects.filter(Q(user_id = request.user) | Q(is_global = True))
            industries = Industry.objects.filter(Q(user_id = request.user) | Q(is_global = True))
            area = Regulator.objects.filter(Q(user_id = request.user) | Q(is_global = True))
            acts = Act.objects.filter(Q(user_id = request.user) | Q(is_global = True))
            
            label = Activity_Labels.objects.filter(Q(user_id = request.user) | Q(is_global = True))

            my_activities = Activity.objects.filter(Q(user_id = request.user) & Q(is_global = False))
            non_global_activity = []
        context_data = {
            "error":error,
            'activities': activities,
            'audittypes': audit_types,
            'entities': entities,
            'industries': industries,
            'acts': acts,
            'label' : label,
            'my_activities':my_activities,
            'non_global_activity':non_global_activity
        }
        return render(request, "master/activity_master.html",context_data)
    else:
        return redirect('render_activity_master')

@login_required
def get_entities(request):
    if request.method == "POST":
        activity_id = request.POST.get('edit_activity_id')
        activity_entities = ActivityAuditTypeEntity.objects.values_list('entity_id').filter(activity_id=activity_id)
        activity_audittype = ActivityAuditTypeEntity.objects.values_list('audittype_id').filter(activity_id=activity_id)
        activity_industry = ActivityAuditTypeEntity.objects.values_list('industry_id').filter(activity_id=activity_id)
        act = Activity.objects.get(pk=activity_id).act
        label = Activity.objects.get(pk=activity_id).label_id
        desc = Activity.objects.get(pk=activity_id).activity_description
        # print(desc)
        activity_name = Activity.objects.get(pk=activity_id).activity_name
        print(label)
        entities = []
        audittype = []
        industries = []
        for entity in activity_entities:
            entities.append(entity)

        for audit in activity_audittype:
            audittype.append(audit)

        for industry in activity_industry:
            industries.append(industry)

        print(entities)
        print(audittype)
        return JsonResponse({'entities' : entities,'audittype':audittype,'act': act.id,'industries':industries,'label':label,'name':activity_name,'desc':desc})

@login_required
def edit_activity(request):
    if request.method == 'POST':
        print("editing")
        activityId = request.POST.get('edit_activity_id')
        activityName = request.POST.get('edit_activity_name')
        activityDescription = request.POST.get('edit_activity_description')
        
        act = request.POST.get('edit_act')
        label = request.POST.get('edit_label')
        entities = request.POST.getlist('edit_entities')
        industries = request.POST.getlist('edit_industries')
        audit_type = request.POST.getlist('edit_audittype')
        print("Edit Activity : ",activityId , activityName ,activityDescription, act , label , industries , audit_type,entities)
        e = list()
        i = list()
        a = list()

        for z in entities:
            e.append(Entity.objects.get(pk=z))

        for z in industries:
            i.append(Industry.objects.get(pk=z))

        for z in audit_type:
            a.append(AuditType.objects.get(pk=z))

        activity = Activity.objects.get(pk = activityId)
        print(activity)
        activitymap = ActivityAuditTypeEntity.objects.filter(activity_id=activityId).distinct()
        for activitydelete in activitymap:
            activitydelete.delete()
        # activitymap = ActivityAuditTypeEntity.objects.filter(activity_id=activityId).distinct().delete()
        activity.activity_name = activityName
        activity.activity_description = activityDescription
        activity.act = Act.objects.get(pk=act)
        activity.label = Activity_Labels.objects.get(pk=label)
        
        activity.save()
        print(activitymap)
        try:      
            task_mappings = ActivityAuditTypeEntity.objects.values().filter(activity=activity)
            print(task_mappings)     
            for industry in i:
                for audittype in a:
                    for entity in e:
                        ActivityAuditTypeEntity.objects.create(
                            activity = activity,
                            audittype = audittype,
                            entity = entity,
                            industry = industry
                        )

            activity.save()
        
            print("Add")
            clients = Client.objects.all()
            
            tasks = Task.objects.filter(activity_id = activityId)
            print(tasks)
            for task in tasks:
                for client in clients:
                    client_details = ClientIndustryAuditTypeEntity.objects.filter(client=client)
                    for client_detail in client_details:
                        audit_plan = AuditPlanMapping.objects.filter(client_id = client.id)
                        for ap in audit_plan:
                            tms = ActivityAuditTypeEntity.objects.filter(activity_id = activityId,audittype = ap.audittype)
                            print(tms)
                            for nt in tms:
                                client_task = ClientTask.objects.filter(auditplan_id = ap.id)
                                cnt = ClientTask.objects.filter(auditplan_id = ap.id,task_name = task.task_name).count()
                                print("Default add")
                                if ap.is_audit_plan_locked == 0 and cnt == 0: 
                                    print("=========ADDING========")
                                    new = ClientTask(
                                                task_name=task.task_name,
                                                task_estimated_days=task.task_estimated_days,
                                                task_auditing_standard=task.task_auditing_standard,
                                                task_international_auditing_standard=task.task_international_auditing_standard,
                                                activity=Activity.objects.get(id=activityId),
                                                client=client,
                                                act = activity.act,
                                                auditplan_id = ap.id
                                            )
                                    new.save()
                                # print(client_task)
                                        
            print("check hoga ab")
            ccs = Client.objects.all()
            for client in ccs:
                audit_plans = AuditPlanMapping.objects.filter(client_id = client.id)
                print(audit_plans)
                mila = 1
                cts = []
                activity_map = []
                for ap in audit_plans:
                    client_details = ClientIndustryAuditTypeEntity.objects.values_list('industry_id','entity_id','audittype_id').filter(client_id = client.id,audittype_id = ap.audittype_id)
                    print(client_details)
                    if ap.is_audit_plan_locked == 0:
                        print("check audit plan")
                        ctss = ClientTask.objects.filter(auditplan_id = ap.id)
                        for ct in ctss:
                            print("AUDIT PLAN AUDIT TYPE : ",ap.audittype)
                            activity_map = ActivityAuditTypeEntity.objects.values_list('industry_id','entity_id','audittype_id').filter(activity_id = ct.activity_id,audittype_id = ap.audittype_id)
                            print(activity_map)
                            for cd in client_details:
                                # print(cd[0])
                                for am in activity_map:
                                    if am == cd:
                                        print("==",am," = ",cd)
                                        mila = 1
                                        break
                                    else:
                                        print("!=",am," = ",cd)
                                        mila = 0
                                if mila == 1:
                                    break
                            print(mila)
                            if not mila == 0:
                                print("Add")
                            else:
                                print("removing")
                                ClientTask.objects.filter(pk=ct.id).delete()
                                cts.append(ct.id)
                                
                print(cts)
        except Exception as e:
            print(e)                                    
    
    return HttpResponseRedirect("/main_client/activities") 
        # return HttpResponseRedirect("/main_client/acts") 

@login_required
def edit_id_activity(request):
    print("yupp")
    if request.method == "POST":
        activity_id = request.POST.get('activity_id')
        if activity_id:
            print(activity_id)
            activity = Activity.objects.get(id=activity_id)
            activity_entities = ActivityAuditTypeEntity.objects.values_list('entity_id').filter(activity_id=activity_id)
            activity_audittype = ActivityAuditTypeEntity.objects.values_list('audittype_id').filter(activity_id=activity_id)
            activity_industry = ActivityAuditTypeEntity.objects.values_list('industry_id').filter(activity_id=activity_id)
            act = Activity.objects.get(pk=activity_id).act
            label = Activity.objects.get(pk=activity_id).label_id
            desc = Activity.objects.get(pk=activity_id).activity_description
            # print(desc)
            activity_name = Activity.objects.get(pk=activity_id).activity_name
            print(label)
            entities = []
            audittype = []
            industries = []
            for entity in activity_entities:
                entities.append(entity)

            for audit in activity_audittype:
                audittype.append(audit)

            for industry in activity_industry:
                industries.append(industry)

            print(entities)
            print(audittype)
            return JsonResponse({'activity_id':activity.id,'activity_name':activity.activity_name,'entities' : entities,'audittype':audittype,'act': act.id,'industries':industries,'label':label,'name':activity_name,'desc':desc})
    return HttpResponseRedirect("/main_client/activities")

@login_required
def remove_activity(request, activity_id):
    if activity_id:
        activity = Activity.objects.filter(pk = activity_id)
        activity.delete()
        return HttpResponseRedirect("/main_client/activities") 
        
# ------------------------------------------------End Activity---------------------------------

# -----------------------------------Entity--------------------------------------

@login_required
def render_entity_master(request):
    if request.method == 'GET':
        # Get values from master
        if request.user.is_super_admin:
            entities = Entity.objects.filter(Q(is_global=True))
            my_entities = Entity.objects.filter(Q(is_global=True))
            non_global_entity = Entity.objects.filter(Q(is_global=False))
        else:
            entities = Entity.objects.filter(Q(user_id = request.user.id) | Q(is_global=True))
            my_entities = Entity.objects.filter(Q(user_id = request.user.id) & Q(is_global=False))
            non_global_entity = []
        # Pass it to the template
        context_data = {
            'entities': entities,
            'my_entities':my_entities,
            'non_global_entity':non_global_entity
        }
        return render(request, "master/entity_master.html",context_data)

@login_required
def entity_make_global(request,entity_id):
    print(entity_id)
    entity = Entity.objects.get(id = entity_id)
    entity.is_global = True
    entity.save()
    return HttpResponseRedirect("/main_client/entities")

@login_required
def add_entity(request):
    if request.method == 'POST':
        
        entity_name = request.POST.get('entity_name')

        is_there = Entity.objects.filter((Q(entity_name=entity_name) & Q(user_id=request.user.id)) | (Q(entity_name=entity_name) & Q(is_global=True))).exists()
        
        error = ""
        if is_there:
            error = "Entity exists with name: " + str(entity_name)
        else:
            if request.user.is_super_admin:
                new_entity = Entity(user=request.user,entity_name=entity_name,is_global=True)
            else:
                new_entity = Entity(user=request.user,entity_name=entity_name)
            try:
                new_entity.save()
                return HttpResponseRedirect('/main_client/entities')
            except Exception as e:
                raise e
        
        if request.user.is_super_admin:
            entities = Entity.objects.filter(Q(is_global=True))
            my_entities = Entity.objects.filter(Q(is_global=True))
            non_global_entity = Entity.objects.filter(Q(is_global=False))
        else:
            entities = Entity.objects.filter(Q(user_id = request.user.id) | Q(is_global=True))
            my_entities = Entity.objects.filter(Q(user_id = request.user.id) & Q(is_global=False))
            non_global_entity = []
        # Pass it to the template
        context_data = {
            "error":error,
            'entities': entities,
            'my_entities':my_entities,
            'non_global_entity':non_global_entity
        }
        return render(request, "master/entity_master.html",context_data)
    else:
        return redirect('render_entity_master')

@login_required
def edit_entity(request):
    if request.method == 'POST':
        entityId = request.POST.get('edit_entity_id')
        entityName = request.POST.get('edit_entity_name')
        
        entity = Entity.objects.get(pk = entityId)
        entity.entity_name = entityName

        try:
            entity.save()
        except Exception as e:
            print(e)
        
        return HttpResponseRedirect("/main_client/entities")

@login_required
def remove_entity(request, entity_id):
    if entity_id:
        entity = Entity.objects.filter(pk = entity_id)
        entity.delete()
        return HttpResponseRedirect("/main_client/entities") 



# -----------------------------------End Entity----------------------------------
@login_required
def upload_task(request):
    if request.method == "POST":
        upload_task_file = request.FILES.get('upload_task_file',False)
        if upload_task_file:
            file_name = upload_task_file.name
            if file_name.endswith('.csv'):
                print("File is csv")
                file_data = upload_task_file.read().decode("utf-8")		

                lines = file_data.split("\n")
                #loop over the lines and save them in db. If error , store as string and then display
                main_list = []
                for line in lines:						
                    fields = line.split(",")
                    data_dict = {}
                    data_dict["id"] = fields[0]
                    data_dict["task_name"] = fields[1]
                    data_dict["task_estimated_days"] = fields[2]
                    data_dict["task_auditing_standard"] = fields[3]
                    data_dict["task_international_auditing_standard"] = fields[4]
                    data_dict["activity"] = fields[5]
                    if data_dict['id'] == 'id':
                        print("data is same hence not uploaded")
                    else:
                        main_list.append(data_dict)
                for i in main_list:
                    activity_id = i['activity']
                    add_task = Task(id=i['id'],task_name=i['task_name'], task_estimated_days=i['task_estimated_days'], 
                                task_auditing_standard=i['task_auditing_standard'], task_international_auditing_standard=i['task_international_auditing_standard'],
                                activity=Activity.objects.get(pk=activity_id))
                    add_task.save()

    return redirect("/main_client/tasks")


@login_required
def add_task(request):
    if request.method == "POST":
        task_name = request.POST.get('task_name')
        estimated_hours = request.POST.get('estimated_hours')
        estimated_minutes = request.POST.get('estimated_minutes')
        print(type(estimated_hours) , type(estimated_minutes))
        estimated_hours = int(estimated_hours)
        estimated_minutes = int(estimated_minutes)
        estimated_days = (estimated_hours * 60) + estimated_minutes
        print("total minutes :",estimated_days)
        
        auditing_standard = request.POST.get('auditing_standard')
        international_auditing_standard = request.POST.get('international_auditing_standard')
        activity = request.POST.get('activity')

        is_there = Task.objects.filter((Q(task_name=task_name) & Q(user_id=request.user.id)) | (Q(task_name=task_name) & Q(is_global=True))).exists()
        
        # print(uploaded_attachment_filename)
        error = ""
        if is_there:
            error = "Task exists with name: " + str(task_name)
        else:
            if request.user.is_super_admin:
                task = Task(user=request.user,task_name=task_name, task_estimated_days=estimated_days, 
                    task_auditing_standard=auditing_standard, task_international_auditing_standard=international_auditing_standard,
                        activity=Activity.objects.get(pk=activity),is_global=True)
            else:
                task = Task(user=request.user,task_name=task_name, task_estimated_days=estimated_days, 
                    task_auditing_standard=auditing_standard, task_international_auditing_standard=international_auditing_standard,
                        activity=Activity.objects.get(pk=activity))
            try:
                task.save()
            except Exception as e:
                raise e
        print(error)
        if request.user.is_super_admin:
            tasks=Task.objects.filter(is_global=True)
        else:
            tasks = Task.objects.filter(Q(is_global=True) | Q(user_id = request.user.id))
        task=Task.objects.get(task_name = task_name)
        task_id = Task.objects.get(task_name = task_name)
        
        attachment = request.FILES.get('attachment', False)
        print(attachment)
        if attachment:
            attachment_file = FilesStorage(request,request.user,"task",task,"task_process_notes",request.FILES['attachment'])
            # main_client = User.objects.get(id = request.user.id)
            # max_files = MaxFiles.objects.get(main_client=main_client.id)
            # if max_files.max_files == max_files.current_files:
            #     print("give error")
            #     error = "Maximum number of files exceeded"
            # else:
            #     print("save the file")
            #     path = str(settings.MEDIA_ROOT) + '\\clients\\'+ str(main_client.username) + '\\'
            #     directory = 'activity_process_notes'
            #     dire = os.path.join(path, directory)
            #     print(dire) 

            #     uploaded_filename = request.FILES['attachment'].name    
            #     try:
            #         os.makedirs(dire)
            #         print("created folder")
            #     except:
            #         print("folder already created")
            #         pass
            #     task_file_upload_path = str(dire) + '\\'
            #     try:
            #         os.makedirs(task_file_upload_path)
            #         print("created folder")
            #     except:
            #         print("folder already created")
            #         pass
            #     full_filename = os.path.join(task_file_upload_path, uploaded_filename)
            #     fout = open(full_filename, 'wb+')
            #     print("full_filename :",full_filename)

            #     file_content = ContentFile( request.FILES['attachment'].read() )

            #     # Iterate through the chunks.
            #     for chunk in file_content.chunks():
            #         fout.write(chunk)
            #     fout.close()
            #     remove_absolute_path = full_filename.replace(str(settings.MEDIA_ROOT),'')
            #     print("removed path :",remove_absolute_path)
            #     task.process_notes.name = remove_absolute_path
                
            #     task.save()
            #     max_files.current_files = int(max_files.current_files) + 1
            #     max_files.save()
            # uploaded_attachment_filename = request.FILES[u'attachment'].name
            # uploaded_attachment_file = request.FILES['attachment']
            # uploaded_attachment_filename = str(task_id) + "/" +  uploaded_attachment_filename
            # task.process_notes.save(uploaded_attachment_filename, uploaded_attachment_file)
            # task.save()
        # print(tasks)
        if request.user.is_super_admin:
            tasks = Task.objects.filter(Q(is_global = True))
            activities = Activity.objects.filter(Q(is_global = True))
            my_tasks = Task.objects.filter(Q(is_global = True))
            non_global_task = Task.objects.filter(Q(is_global = False))
        else:
            tasks = Task.objects.filter(Q(user_id = request.user) | Q(is_global = True))
            activities = Activity.objects.filter(Q(user_id = request.user) | Q(is_global = True))
            my_tasks = Task.objects.filter(Q(user_id = request.user) & Q(is_global = False))
            non_global_task = []
        context_data = {
            "error":error,
            'tasks': tasks,
            'activities': activities,
            "my_tasks":my_tasks,
            'non_global_task':non_global_task
        }
        clients = Client.objects.all()
        task_mappings = ActivityAuditTypeEntity.objects.filter(activity=activity)
        for client in clients:
            client_details = ClientIndustryAuditTypeEntity.objects.filter(client=client)
            for client_detail in client_details:
                for new_task in task_mappings:
                    if (client_detail.audittype_id == new_task.audittype_id) and (client_detail.entity_id == new_task.entity_id) and  (client_detail.industry_id==new_task.industry_id):
                        print("match")
                        is_there = ClientTask.objects.filter(client=client).filter(task_name=task_name).exists()
            # print(is_there)
                        error = ""
                        if is_there:
                            error = "Task exists with name: " + str(task_name) 
                        else:
                            audit_plan = AuditPlanMapping.objects.filter(client_id = client.id)
                            for ap in audit_plan:
                                if ap.is_audit_plan_locked == False:
                                    newTask = ClientTask(
                                        task_name=task_name,
                                        task_estimated_days=estimated_days,
                                        task_auditing_standard=auditing_standard,
                                        task_international_auditing_standard=international_auditing_standard,
                                        activity=Activity.objects.get(id=activity),
                                        # act=Act.objects.get(id=acti.act_id),
                                        client=client,
                                        auditplan_id = ap.id
                                    )
                                    newTask.save()
                # print(activity)
        return render(request, "master/task_master.html",context_data)
    else:
        return redirect('render_task_master')

@login_required
def render_task_master(request):
    if request.method == 'GET':
        if request.user.is_super_admin:
            tasks = Task.objects.filter(Q(is_global = True))
            activities = Activity.objects.filter(Q(is_global = True))
            my_tasks = Task.objects.filter(Q(is_global = True))
            non_global_task = Task.objects.filter(Q(is_global = False))
        else:
            tasks = Task.objects.filter(Q(user_id = request.user) | Q(is_global = True))
            activities = Activity.objects.filter(Q(user_id = request.user) | Q(is_global = True))
            my_tasks = Task.objects.filter(Q(user_id = request.user) & Q(is_global = False))
            non_global_task = []
        context_data = {
            'tasks': tasks,
            'activities': activities,
            "my_tasks":my_tasks,
            'non_global_task':non_global_task
        }
    
        return render(request, "master/task_master.html",context_data)


@login_required
def task_make_global(request,task_id):
    print(task_id)
    task = Task.objects.get(id = task_id)
    task.is_global = True
    task.save()
    return HttpResponseRedirect("/main_client/tasks")

@login_required
def crud_processed_notes(request):
    if request.method == "POST":
        process_task_id = request.POST.get('process_task_id')
        process_notes_file = request.FILES.get('process_notes_file',False)

        if process_task_id and process_notes_file:
                attachment_file = FilesStorage(request,request.user,'task',process_task_id,"task_update_upload",request.FILES['process_notes_file'])
            # task = Task.objects.get(id = process_task_id)
            # main_client = User.objects.get(id = request.user.id)
            # max_files = MaxFiles.objects.get(main_client=main_client.id)
            # if max_files.max_files == max_files.current_files:
            #     print("give error")
            #     error = "Maximum number of files exceeded"
            # else:
            #     print("save the file")
            #     get_previous_file = task.process_notes
                
            #     path = str(settings.MEDIA_ROOT) + '\\clients\\'+ str(main_client.username) + '\\'
            #     directory = 'activity_process_notes'
            #     dire = os.path.join(path, directory)

            #     uploaded_filename = request.FILES['process_notes_file'].name    
            #     try:
            #         os.makedirs(dire)
            #         print("created folder")
            #     except:
            #         print("folder already created")
            #         pass
            #     task_file_upload_path = str(dire) + '\\'
            #     try:
            #         os.makedirs(task_file_upload_path)
            #         print("created folder")
            #     except:
            #         print("folder already created")
            #         pass
            #     if get_previous_file:
            #         print(get_previous_file)
            #         try:
            #             os.remove(str(settings.MEDIA_ROOT) + str(get_previous_file))
                        
                        
            #         except Exception as e:
            #             print("error :",e)
            #         full_filename = os.path.join(task_file_upload_path, uploaded_filename)
            #         fout = open(full_filename, 'wb+')
            #         print("full_filename :",full_filename)

            #         file_content = ContentFile(request.FILES['process_notes_file'].read())

            #         # Iterate through the chunks.
            #         for chunk in file_content.chunks():
            #             fout.write(chunk)
            #         fout.close()
            #         remove_absolute_path = full_filename.replace(str(settings.MEDIA_ROOT),'')
            #         print("removed path :",remove_absolute_path)
            #         task.process_notes.name = remove_absolute_path
                    
            #         task.save()
            #     else:
            #         full_filename = os.path.join(task_file_upload_path, uploaded_filename)
            #         fout = open(full_filename, 'wb+')
            #         print("full_filename :",full_filename)

            #         file_content = ContentFile(request.FILES['process_notes_file'].read())

            #         # Iterate through the chunks.
            #         for chunk in file_content.chunks():
            #             fout.write(chunk)
            #         fout.close()
            #         remove_absolute_path = full_filename.replace(str(settings.MEDIA_ROOT),'')
            #         print("removed path :",remove_absolute_path)
            #         task.process_notes.name = remove_absolute_path
                    
            #         task.save()
            #         max_files.current_files = int(max_files.current_files) + 1
            #         max_files.save()
                return JsonResponse({'saved':'yes'})


        task_id = request.POST.get('task_id')
        if task_id:
            print("task_id :",task_id)
            task = Task.objects.get(id = task_id)
            if task.process_notes:
                obj = {
                    'process_notes':str(task.process_notes)
                }
            else:
                obj = {
                    'process_notes':'none'
                }
            return JsonResponse({'data':obj})
    return HttpResponseRedirect('/main_client/tasks')

@login_required
def get_activities(request):
    if request.method == "POST":
        task_id = request.POST.get('task_id')
        task = Task.objects.get(id=task_id)
        activity = Task.objects.get(pk=task_id).activity.id
        if task.task_estimated_days:
            hours = int(task.task_estimated_days) // 60
            minutes = int(task.task_estimated_days) % 60
            print(hours , minutes)
        else:
            hours = 0
            minutes = 0
        return JsonResponse({'task':task.id,'activity' : activity,'task_auditing_standard':task.task_auditing_standard,'task_international_auditing_standard':task.task_international_auditing_standard,'hours':hours,'minutes':minutes})

@login_required
def edit_task(request):
    if request.method == 'POST':
        taskId = request.POST.get('edit_task_id')
        taskName = request.POST.get('edit_task_name')
        edit_estimated_hours = request.POST.get('edit_estimated_hours')
        edit_estimated_minutes = request.POST.get('edit_estimated_minutes')
        edit_estimated_hours = int(edit_estimated_hours)
        edit_estimated_minutes = int(edit_estimated_minutes)
        estimated_days = (edit_estimated_hours * 60) + edit_estimated_minutes
        print("total minutes :",estimated_days)
        taskAuditStandard = request.POST.get('edit_auditing_standard')
        taskIntlAuditStandard = request.POST.get('edit_international_auditing_standard')
        activity = request.POST.get('edit_activity')
        task = Task.objects.get(pk = taskId)
        
        clients = Client.objects.all()
        for client in clients:
            audit_plans = AuditPlanMapping.objects.filter(client_id = client.id)
            for ap in audit_plans:
                if ap.is_audit_plan_locked == 0:
                    client_tasks = ClientTask.objects.filter(task_name = task.task_name,auditplan_id = ap.id)
                    print("Client task: ",client_tasks)
                    if client_tasks.count() != 0:
                        for ct in client_tasks:
                            ct.task_name = taskName
                            ct.task_estimated_days = estimated_days
                            ct.task_auditing_standard = taskAuditStandard
                            ct.task_international_auditing_standard = taskIntlAuditStandard
                            if activity == task.activity:
                                print("Activity same change")
                                ct.activity = Activity.objects.get(pk=activity)
                                ct.save()
                            else:
                                clientmappings = ClientIndustryAuditTypeEntity.objects.filter(client_id = client.id,audittype_id = ap.audittype_id)
                                activitymappings = ActivityAuditTypeEntity.objects.filter(activity_id = activity,audittype_id=ap.audittype_id)
                                flag = 1
                                for cm in clientmappings:
                                    for am in activitymappings:
                                    # print("Enitity=",cm.entity_id,"Industry=",cm.industry_id,"Audit type=",cm.audittype_id)
                                    # print("Enitity=",am.entity_id,"Industry=",am.industry_id,"Audit type=",am.audittype_id)
                                        if am.entity_id == cm.entity_id and am.industry_id == cm.industry_id:
                                            flag = 0


                                if flag == 0:
                                    print("Activity change")
                                    ct.activity = Activity.objects.get(pk=activity)
                                    ct.save()
                                    
                                else:
                                    print("Activity delete")
                                    ct.delete()
                    else:
                        clientmappings = ClientIndustryAuditTypeEntity.objects.filter(client_id = client.id,audittype_id = ap.audittype_id)
                        activitymappings = ActivityAuditTypeEntity.objects.filter(activity_id = activity,audittype_id=ap.audittype_id)
                        flag = 1
                        for cm in clientmappings:
                            for am in activitymappings:
                                if am.entity_id == cm.entity_id and am.industry_id == cm.industry_id:
                                    print("new task!!!")
                                    newTask = ClientTask(
                                        task_name=taskName,
                                        task_estimated_days=estimated_days,
                                        task_auditing_standard=taskAuditStandard,
                                        task_international_auditing_standard=taskAuditStandard,
                                        activity=Activity.objects.get(id=activity),
                                        # act=Act.objects.get(id=acti.act_id),
                                        client=client,
                                        auditplan_id = ap.id
                                    )
        task.task_name = taskName
        task.task_estimated_days = estimated_days
        task.task_auditing_standard = taskAuditStandard
        task.task_international_auditing_standard = taskIntlAuditStandard
        task.activity = Activity.objects.get(pk=activity)
        

        # print(activity," = ",task.activity_id)

        # if task.activity != activity:
        #     print("change")
        # else:
        #     print("no change")
        try:
            task.save()
            newTask.save()
            print("task master change")
        except Exception as e:
            print(e)
        
        return HttpResponseRedirect("/main_client/tasks") 

@login_required
def remove_task(request, task_id):
    if task_id:
        task = Task.objects.get(pk = task_id)
        print(task)
        client_tasks = ClientTask.objects.filter(task_name = task.task_name)
        for ct in client_tasks:
            audit_plan_id = ct.auditplan_id
            ap_locked = AuditPlanMapping.objects.filter(pk = audit_plan_id)
            for ap in ap_locked:
                if ap.is_audit_plan_locked:
                    print("dont delete")
                else:
                    ct.delete()
        task.delete()
        return HttpResponseRedirect("/main_client/tasks") 






def get_all_managers(request):
    if request.method == "POST":
        partner_id = request.POST.get("partner_id")
        all_managers = []
        if partner_id:
            
            get_all_managers = User.objects.filter(linked_employee = partner_id)
            for i in get_all_managers:
                data = {
                    "id": i.id,
                    "username": i.username,
                }
                all_managers.append(data)
                

        return JsonResponse({'data':all_managers})


def get_all_users(request):
    if request.method == "POST":
        manager_id = request.POST.get("manager_id")
        all_users = []
        if manager_id:
            print(manager_id)
            get_all_users = User.objects.filter(linked_employee = manager_id)
            for i in get_all_users:
                data = {
                    "id": i.id,
                    "username": i.username,
                }
                all_users.append(data)
        print("All Users :",all_users)   

        return JsonResponse({'data':all_users})



@login_required
def main_client_assign_task_to_employee(request, client_id):
    if request.method == 'POST':
        partner_id = request.POST.get("partner_id")
        if partner_id:
            partner = request.POST.get(f'partner_{partner_id}')
            manager = request.POST.get(f'manager_{partner_id}')
            users = request.POST.get(f'users_{partner_id}')
        print("partner :",partner,"manager :",manager,"users :",users)
        

        task_id = request.POST.get('task_id')
        task_type = request.POST.get('task_type')
        # print(user_id)
        # print(task_id)
        task_relevance = request.POST.get('task_relevance')
        volume = request.POST.get('volume')
        samplerate = request.POST.get('samplerate')
        user = ''
        if users and manager and partner:
            user = User.objects.get(pk = users)
        elif not user and manager and partner:
            user = User.objects.get(pk = manager)
        elif not user and not manager and partner:
            user = User.objects.get(pk = partner)
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
                # send_mail("Task Assignment", msg, 'icraftsolution.com@gmail.com',[user.email], fail_silently=False)
        except Exception as e:
            print(e)
        return HttpResponseRedirect(f"/main_client/client/{client_id}/tasks/")


