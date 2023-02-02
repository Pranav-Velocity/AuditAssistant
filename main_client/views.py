import re
from django.db.models.fields import NullBooleanField
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

# Create your views here.
@login_required
def Dashboard(request):
    if request.user.is_main_client:
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
            print(remaining_days)
            if (remaining_days <= 30):
                get_expiry_days = remaining_days
        except BillingDetails.DoesNotExist:
            pass
        try:
            get_max_files = MaxFiles.objects.get(main_client = request.user.id)
        except MaxFiles.DoesNotExist:
            get_max_files = ""
        all_linked_users = []
        all_client_tasks = []
        get_users = User.objects.filter(linked_employee = request.user.id)
        for i in get_users:
            get_client_tasks = ClientTask.objects.filter(user = i)
            for ii in get_client_tasks:
                all_client_tasks.append(ii)
            get_users2 = User.objects.filter(linked_employee = i.id)
            for j in get_users2:
                get_client_tasks2 = ClientTask.objects.filter(user = j)
                for k in get_client_tasks2:
                    all_client_tasks.append(k)
                all_linked_users.append(j)
            all_linked_users.append(i)
        partner_uploads = 0
        manager_uploads = 0
        auditor_uploads = 0
        article_uploads = 0


        for i in all_client_tasks:
            print(i.partner_attachment_file , i.manager_attachment_file , i.auditor_attachment_file , i.article_attachment_file)
            if i.partner_attachment_file:
                partner_uploads += 1
            if i.manager_attachment_file:
                manager_uploads += 1
            if i.auditor_attachment_file:
                auditor_uploads += 1
            if i.article_attachment_file:
                article_uploads += 1
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
        
        params = {
            "total_users":len(all_linked_users),
            "total_files":partner_uploads + manager_uploads + auditor_uploads + article_uploads,
            "max_files":get_max_files,
            "message":message,
            "message2":message2,
            "bill_expire_remaining_days":get_expiry_days
        }
        return render(request,"main_client/dashboard.html",params)

@csrf_exempt
def paymentsuccess(request):
    get_billing_details = BillingDetails.objects.get(Q(main_client = request.user.id) & Q(is_active = True))
    user = User.objects.get(id=request.user.id)
    
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
        till_date = date.today() + timedelta(days=delta.days) + timedelta(days=365)
        get_billing_details.is_active = False
        get_billing_details.save()
        create_new_billing_details = BillingDetails(
            main_client = get_main_client.id,
            account_type = "Purchased",
            start_date = date.today(),
            end_date = till_date,
            current_date =  date.today(),
            amount=amount,
            transactionID=txnid,
            payment_status="Realised",
            remarks="Purchased",
            created_by = request.user.id
        )
        create_new_billing_details.save()
        get_latest_transaction = TempTransaction.objects.latest('id')
        get_all_except_latest_transaction = TempTransaction.objects.filter(~Q(id=get_latest_transaction.id))
        get_all_except_latest_transaction.delete()
    
    params = {
        "user":User.objects.get(id=request.user.id),
        "bill":BillingDetails.objects.get(Q(main_client = request.user.id) & Q(is_active = True))
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
        employee_fname = request.POST.get('employee_fname')
        employee_lname = request.POST.get('employee_lname')
        employee_username = request.POST.get('employee_username')
        employee_password = request.POST.get('employee_password')
        employee_email = request.POST.get('employee_email')
        role = request.POST.get('role')        
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
                        linked_employee=user_id
                    )
                    
                elif role == "auditor":
                    new_user = User(username=employee_username, 
                        first_name=employee_fname, 
                        last_name=employee_lname,
                        is_auditorclerk=True,
                        email = employee_email,
                        password = make_password(employee_password),
                        linked_employee=user_id
                    )
                elif role == "article":
                    new_user = User(username=employee_username, 
                        first_name=employee_fname, 
                        last_name=employee_lname,
                        is_articleholder=True,
                        email = employee_email,
                        password = make_password(employee_password),
                        linked_employee=user_id
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
    
    all_users = User.objects.filter(linked_employee = user_id)
    user_lists = []
    for i in all_users:
        user_lists.append(i)
        heirarchy_users = User.objects.filter(linked_employee = i.id)
        for j in heirarchy_users:
            user_lists.append(j)
    print(user_lists)
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
        get_users = User.objects.filter(linked_employee = request.user.id)
        for i in get_users:
            get_client_tasks = ClientTask.objects.filter(user = i)
            for ii in get_client_tasks:
                all_client_tasks.append(ii)
            get_users2 = User.objects.filter(linked_employee = i.id)
            for j in get_users2:
                get_client_tasks2 = ClientTask.objects.filter(user = j)
                for k in get_client_tasks2:
                    all_client_tasks.append(k)
        
        data = []
        for task in all_client_tasks:
            print(task)
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
            "users":student_data
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