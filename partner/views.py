import re
from django.db.models.fields import NullBooleanField
from django.db.models.query import RawQuerySet
from django.shortcuts import render, HttpResponseRedirect, HttpResponse, redirect
from . models import Regulator,UserLink, Act, Activity, Industry, Task, Client, Entity, AuditType, ActivityAuditTypeEntity, ClientIndustryAuditTypeEntity,AuditPlanMapping
from auditapp.models import User
from main_client.models import MaxUsers,MaxFiles
from django.core.mail import send_mail
from datetime import datetime
from django.http import JsonResponse
from django.core import serializers
from .serializers import ClientTaskSerializer
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.conf import settings
from django.db.models import Count
from partner.models import ClientTask, Audits,Activity_Labels
from django.db.models import Exists,Sum
from datetime import timedelta, date
from .models import AuditType, ClientTask
from django.contrib.auth import authenticate
import locale
import csv
import json
from babel.numbers import format_currency
import os
from django.core.files.base import ContentFile

import imaplib
import email
from email.header import decode_header
import webbrowser

def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)

def test(request):
    username = "chandrakant.belell@velocityconsultancy.com"
    password = "&4wE#aGY_Q4Z8ddJ"
    imap_server = "imap.ionos.com"
    imap = imaplib.IMAP4_SSL(imap_server)
    # authenticate
    imap.login(username, password)
    status, messages = imap.select("INBOX")
    # number of top emails to fetch
    N = 3
    # total number of emails
    messages = int(messages[0])
    for i in range(messages, messages-N, -1):
        # fetch the email message by ID
        res, msg = imap.fetch(str(i), "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                # parse a bytes email into a message object
                msg = email.message_from_bytes(response[1])
                # decode the email subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    # if it's a bytes, decode to str
                    subject = subject.decode(encoding)
                # decode email sender
                From, encoding = decode_header(msg.get("From"))[0]
                if isinstance(From, bytes):
                    From = From.decode(encoding)
                print("Subject:", subject)
                print("From:", From)
                # if the email message is multipart
                if msg.is_multipart():
                    # iterate over email parts
                    for part in msg.walk():
                        # extract content type of email
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        try:
                            # get the email body
                            body = part.get_payload(decode=True).decode()
                        except:
                            pass
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            # print text/plain emails and skip attachments
                            print(body)
                        # elif "attachment" in content_disposition:
                        #     # download attachment
                        #     filename = part.get_filename()
                        #     if filename:
                        #         folder_name = clean(subject)
                        #         if not os.path.isdir(folder_name):
                        #             # make a folder for this email (named after the subject)
                        #             os.mkdir(folder_name)
                        #         filepath = os.path.join(folder_name, filename)
                        #         # download attachment and save it
                        #         open(filepath, "wb").write(part.get_payload(decode=True))
                else:
                    # extract content type of email
                    content_type = msg.get_content_type()
                    # get the email body
                    body = msg.get_payload(decode=True).decode()
                    if content_type == "text/plain":
                        # print only text email parts
                        print(body)
                # if content_type == "text/html":
                #     # if it's HTML, create a new HTML file and open it in browser
                #     folder_name = clean(subject)
                #     if not os.path.isdir(folder_name):
                #         # make a folder for this email (named after the subject)
                #         os.mkdir(folder_name)
                #     filename = "index.html"
                #     filepath = os.path.join(folder_name, filename)
                #     # write the file
                #     open(filepath, "w").write(body)
                #     # open in the default browser
                #     webbrowser.open(filepath)
                # print("="*100)
    # close the connection and logout
    imap.close()
    imap.logout()
    return render(request,'test.html')


@login_required
def index(request):
    if request.user.is_partner:
        all_tasks = ClientTask.objects.filter(user=request.user.id,status=False).count()
        all_clients = Client.objects.filter(assigned_partner_id =request.user.id).count()
        ac = Client.objects.filter(assigned_partner_id =request.user.id)
        all_approved_tasks = ClientTask.objects.filter(is_approved_partner=True,client_id__in=ac).count()
        all_rejected_tasks = ClientTask.objects.filter(is_rejected=True,client_id__in=ac).count()
        pending_tasks = ClientTask.objects.filter(is_approved_partner=False,is_completed=False,is_start=True,client_id__in=ac).count()
        completed_tasks = ClientTask.objects.filter(is_approved_partner=True,client_id__in=ac).count()
        rejected_tasks = ClientTask.objects.filter(is_rejected=True,client_id__in=ac).count()
        billable_invoices = AuditPlanMapping.objects.filter(is_billable=True,client_id__in=ac).count()
        invoices_generated = AuditPlanMapping.objects.filter(invoice_number__isnull=False,client_id__in=ac).count()
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
        
        # invoice_details = ClientTask.objects.raw('SELECT client_id FROM partner_clienttask')
        # # print(invoice_details)
        # for i in invoice_details:
        #     print(i)
        context_set={
                    'all_approved_tasks':all_approved_tasks,
                    'all_rejected_tasks':all_rejected_tasks,
                    'all_tasks':all_tasks,
                    'pending_tasks':pending_tasks,
                    'all_clients':all_clients,
                    'completed_tasks':completed_tasks,
                    'rejected_tasks' : rejected_tasks,
                    'billable_invoices':billable_invoices,
                    'invoices_generated':invoices_generated,
                    'invoices_notgenerated':invoices_notgenerated,
                    'invoices_total':total
                    }
        return render(request, 'partner/partner_index.html', context_set)


@login_required
def render_areas_master(request):
    # Get all the areas
    areas = Regulator.objects.all()
    audittypes=Audits.objects.all()
    # Pass it to the template
    context_data = {
        'areas': areas,
        "audittypes" : audittypes
    }
    
    return render(request, "master/areas_master.html",context_data)
        
# ----------------------------------Regulators -------------------------------------
@login_required
def add_area(request):
    if request.method == "POST":
        area_name = request.POST.get('area_name')
        type_of_audit = request.POST.get('types_of_audits')
        is_there = Regulator.objects.filter(area_name=area_name).exists()
        # print(is_there)
        error = ""
        if is_there:
            error = "Regulator exists with name: " + str(area_name)
        else:
            new_area = Regulator(area_name=area_name,type_of_audits=type_of_audit)
            new_area.save()
            return HttpResponseRedirect('/partner/areas')
        
        areas = Regulator.objects.all()
        context_data = {
            "error": error,
            "areas": areas,
        }
        return render(request, "master/areas_master.html", context_data)

@login_required
def remove_area(request, area_id):
    
    if area_id:
        area = Regulator.objects.get(pk = area_id)
        area.delete()
        return HttpResponseRedirect("/partner/areas")  

@login_required
def edit_area(request):

    if request.method == 'POST':
        areaId = request.POST.get('area_id')
        areaName = request.POST.get('area_name')
        type_of_audit = request.POST.get('types_of_audits')
        area = Regulator.objects.get(pk = areaId)
        area.area_name = areaName
        area.type_of_audits = type_of_audit
        area.save()
        return HttpResponseRedirect("/partner/areas") 

# ----------------------------------End Regulators-------------------------------------

# -----------------------------------Acts-----------------------------------------
@login_required
def render_acts_master(request):

    # Get all the acts and areas from the master tables
    acts = Act.objects.all()
    areas = Regulator.objects.all()
    
    # Pass it to the template
    context_data = {
        'acts': acts,
        'areas': areas
    }
    return render(request, 'master/acts_master.html', context_data)


@login_required
def add_act(request):
    if request.method == 'POST':
        #  Get the values from the template
        act_name = request.POST.get('act_name')
        area = request.POST.get('area')

        # Get the area
        area = Regulator.objects.get(id = area)

        # Check if the act exists
        is_there = Act.objects.filter(act_name=act_name).exists()
        
        error = ""
        if is_there:
            error = "Act exists with name: " + str(act_name)
        else:
            # Create a new act
            new_act = Act(act_name=act_name, area=area)
            try:
                # Save it to database
                new_act.save()
                return HttpResponseRedirect('/partner/acts')
            except Exception as e:
                raise e
        
        acts = Act.objects.all()
        areas = Regulator.objects.all()
        context_data = {
            'acts': acts,
            'areas' : areas,
            "error": error,
        }
        return render(request, "master/acts_master.html", context_data) 

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
        
        return HttpResponseRedirect("/partner/acts") 

@login_required
def remove_act(request, act_id):
    if act_id:
        # Get the object from master
        act = Act.objects.get(pk = act_id)

        # Delete it from master
        act.delete()
        return HttpResponseRedirect("/partner/acts") 
# ---------------------------------------------------End Acts----------------------------------

# ------------------------------------------------Audit Type-----------------------------------

@login_required
def render_audittype_master(request):
    if request.method == 'GET':
        # Get all the records from master
        audittypes = AuditType.objects.all()

        # Pass it to template
        context_data = {
            'audittypes': audittypes
        }
        return render(request, "master/audittype_master.html",context_data)

@login_required
def add_audittype(request):
    if request.method == "POST":
        # Get the form values from template
        audittype_name = request.POST.get('audit_type_name')
        
        # Check if already exists
        is_there = AuditType.objects.filter(audit_type_name=audittype_name).exists()
        
        error = ""
        if is_there:
            error = "Audit Type exists with name: " + str(audittype_name)
        else:
            # Create a new Audit type
            new_audittype = AuditType(audit_type_name=audittype_name)
            try:
                # Save it to DB
                new_audittype.save()
                return HttpResponseRedirect('/partner/audittypes')
            except Exception as e:
                print(e)

        audittypes = AuditType.objects.all()
        context_data = {
            'audittypes': audittypes,
            'error': error
        }
        return render(request, "master/audittype_master.html",context_data)  

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
        return HttpResponseRedirect("/partner/audittypes")

@login_required
def remove_audittype(request, audittype_id):
    if audittype_id:
        # Get the audit type from DB
        audittype = AuditType.objects.get(pk = audittype_id)

        # Delete the audit type
        audittype.delete()
        return HttpResponseRedirect("/partner/audittypes") 

# ----------------------------------------End Audit Type -------------------------------

# -----------------------------------Entity--------------------------------------

@login_required
def render_entity_master(request):
    if request.method == 'GET':
        # Get values from master
        entities = Entity.objects.all()

        # Pass it to the template
        context_data = {
            'entities': entities
        }
        return render(request, "master/entity_master.html",context_data)

@login_required
def add_entity(request):
    if request.method == 'POST':
        
        entity_name = request.POST.get('entity_name')

        is_there = Entity.objects.filter(entity_name=entity_name).exists()
        
        error = ""
        if is_there:
            error = "Entity exists with name: " + str(entity_name)
        else:
            new_entity = Entity(entity_name=entity_name)
            try:
                new_entity.save()
                return HttpResponseRedirect('/partner/entities')
            except Exception as e:
                raise e
        
        entities = Entity.objects.all()
        context_data = {
            'entities': entities,
            'error': error
        }
        return render(request, "master/entity_master.html",context_data)

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
        
        return HttpResponseRedirect("/partner/entities")

@login_required
def remove_entity(request, entity_id):
    if entity_id:
        entity = Entity.objects.filter(pk = entity_id)
        entity.delete()
        return HttpResponseRedirect("/partner/entities") 



# -----------------------------------End Entity----------------------------------

# ---------------------------------- Activity Labels --------------------------------

@login_required
def render_activity_label_master(request):
    if request.method == 'GET':
        activity_label = Activity_Labels.objects.all()
        context_data = {
            'activity_label': activity_label
        }
        return render(request, "master/activity_label_master.html",context_data)

@login_required
def add_activitylabel(request):
    if request.method == 'POST':
        activity_label_name = request.POST.get('activity_label_name')
        
        is_there = Activity_Labels.objects.filter(activity_label_name=activity_label_name).exists()
        
        error = ""
        if is_there:
            error = "Activity Label exists with name: " + str(activity_label_name)
        else:
            new_activity_label = Activity_Labels(activity_label_name=activity_label_name)
            try:
                new_activity_label.save()
                return HttpResponseRedirect('/partner/activitylabel')
            except Exception as e:
                print(e)

        activity_label = Activity_Labels.objects.all()
        context_data = {
            'activity_label': activity_label,
            'error': error
        }
        return render(request, "master/activity_label_master.html",context_data)  

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
        return HttpResponseRedirect("/partner/activitylabel")

@login_required
def remove_activitylabel(request, activitylabel_id):
    if activitylabel_id:
        activity_label = Activity_Labels.objects.get(pk = activitylabel_id)
        activity_label.delete()
        return HttpResponseRedirect("/partner/activitylabel") 

# -------------------------------------Industry-----------------------------------------

@login_required
def render_industry_master(request):
    if request.method == 'GET':
        industries = Industry.objects.all()
        context_data = {
            'industries': industries
        }
        return render(request, "master/industry_master.html",context_data)



@login_required
def add_industry(request):
    if request.method == 'POST':
        industry_name = request.POST.get('industry_name')
        
        is_there = Industry.objects.filter(industry_name=industry_name).exists()
        
        error = ""
        if is_there:
            error = "Industry exists with name: " + str(industry_name)
        else:
            new_industry = Industry(industry_name=industry_name)
            try:
                new_industry.save()
                return HttpResponseRedirect('/partner/industries')
            except Exception as e:
                print(e)

        industries = Industry.objects.all()
        context_data = {
            'industries': industries,
            'error': error
        }
        return render(request, "master/industry_master.html",context_data)  

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
        return HttpResponseRedirect("/partner/industries")

@login_required
def remove_industry(request, industry_id):
    if industry_id:
        industry = Industry.objects.get(pk = industry_id)
        industry.delete()
        return HttpResponseRedirect("/partner/industries") 
# -----------------------------------End Industry--------------------------------

# ---------------------------------------------------Activities--------------------------------

@login_required
def render_activity_master(request):
    current_partner = User.objects.get(id = request.user.id)
    main_client = User.objects.get(id = current_partner.linked_employee)
    path = str(settings.MEDIA_ROOT) + '\\clients\\'+ str(main_client.username) + '\\'
    count=0
    for root_dir, cur_dir, files in os.walk(path):
        count += len(files)
    print('file count:', count)
    if request.method == "GET":
        activities = Activity.objects.all()
        audit_types = AuditType.objects.all()
        entities = Entity.objects.all()
        industries = Industry.objects.all()
        acts = Act.objects.all()
        label = Activity_Labels.objects.all()
        context_data = {
            'activities': activities,
            'audittypes': audit_types,
            'entities': entities,
            'industries': industries,
            'acts': acts,
            'label' : label
        }
    
        return render(request, "master/activity_master.html",context_data)

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


        is_there = Activity.objects.filter(activity_name=activity_name).exists()
        
        error = ""
        if is_there:
            error = "Activity exists with name: " + str(activity_name)
        else:
            pass
            activity = Activity(activity_name=activity_name, 
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
                # return HttpResponseRedirect('/partner/activities')
            except Exception as e:
                raise e
        activity_id = Activity.objects.get(activity_name = activity_name)
        activity = Activity.objects.get(activity_name = activity_name)
        # print(activity_id)
        
        attachment = request.FILES.get('attachment', False)
        # print(attachment)
        if attachment:
            current_partner = User.objects.get(id = request.user.id)
            main_client = User.objects.get(id = current_partner.linked_employee)
            max_files = MaxFiles.objects.get(main_client=main_client.id)
            if max_files.max_files == max_files.current_files:
                print("give error")  
                error = "Maximum number of files exceeded"
            else:
                print("save the file")
                path = str(settings.MEDIA_ROOT) + '\\clients\\'+ str(main_client.username) + '\\'
                directory = 'process_notes'
                dire = os.path.join(path, directory)
                print(dire) 

                uploaded_filename = request.FILES['attachment'].name    
                try:
                    os.makedirs(dire)
                    print("created folder")
                except:
                    print("folder already created")
                    pass
                full_filename = os.path.join(dire, uploaded_filename)
                fout = open(full_filename, 'wb+')
                print("full_filename :",full_filename)

                file_content = ContentFile( request.FILES['attachment'].read() )

                # Iterate through the chunks.
                for chunk in file_content.chunks():
                    fout.write(chunk)
                fout.close()
                remove_absolute_path = full_filename.replace(str(settings.MEDIA_ROOT),'')
                print("removed path :",remove_absolute_path)
                activity.process_notes.name = remove_absolute_path
                # uploaded_attachment_filename = request.FILES[u'attachment'].name
                # uploaded_attachment_file = request.FILES['attachment']
                # uploaded_attachment_filename = str(activity_id) + "/" +  uploaded_attachment_filename
                # activity.process_notes.save(uploaded_attachment_filename, uploaded_attachment_file)
                
                # Add to the mapping table
                activity.save()
                max_files.current_files = int(max_files.current_files) + 1
                max_files.save()
        activities = Activity.objects.all()
        acts = Act.objects.all()
        labels = Activity_Labels.objects.all()
        audit_types = AuditType.objects.all()
        entities = Entity.objects.all()
        industries = Industry.objects.all()
        context_data = {
            'activities' : activities,
            'acts': acts,
            'audittypes': audit_types,
            'entities': entities,
            "error": error,
            'labels' : labels,
            'industries' : industries
        } 
        return HttpResponseRedirect("/partner/activities",context_data)

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
    
    return HttpResponseRedirect("/partner/activities") 
        # return HttpResponseRedirect("/partner/acts") 

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
    return HttpResponseRedirect("/partner/activities")

@login_required
def remove_activity(request, activity_id):
    if activity_id:
        activity = Activity.objects.filter(pk = activity_id)
        activity.delete()
        return HttpResponseRedirect("/partner/activities") 
        
# ------------------------------------------------End Activity---------------------------------

# --------------------------------------------------Tasks--------------------------------

@login_required
def render_task_master(request):
    if request.method == 'GET':
        tasks = Task.objects.all()
        activities = Activity.objects.all()
        context_data = {
            'tasks': tasks,
            'activities': activities,
        }
    
        return render(request, "master/task_master.html",context_data)

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

    return redirect("/partner/tasks")


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

        is_there = Task.objects.filter(task_name=task_name).exists()
        
        # print(uploaded_attachment_filename)
        error = ""
        if is_there:
            error = "Task exists with name: " + str(task_name)
        else:
            task = Task(task_name=task_name, task_estimated_days=estimated_days, 
                task_auditing_standard=auditing_standard, task_international_auditing_standard=international_auditing_standard,
                    activity=Activity.objects.get(pk=activity))
            try:
                task.save()
            except Exception as e:
                raise e

        tasks=Task.objects.all()
        task=Task.objects.get(task_name = task_name)
        task_id = Task.objects.get(task_name = task_name)
        
        attachment = request.FILES.get('attachment', False)
        print(attachment)
        if attachment:
            current_partner = User.objects.get(id = request.user.id)
            main_client = User.objects.get(id = current_partner.linked_employee)
            max_files = MaxFiles.objects.get(main_client=main_client.id)
            if max_files.max_files == max_files.current_files:
                print("give error")
                error = "Maximum number of files exceeded"
            else:
                print("save the file")
                path = str(settings.MEDIA_ROOT) + '\\clients\\'+ str(main_client.username) + '\\'
                directory = 'activity_process_notes'
                dire = os.path.join(path, directory)
                print(dire) 

                uploaded_filename = request.FILES['attachment'].name    
                try:
                    os.makedirs(dire)
                    print("created folder")
                except:
                    print("folder already created")
                    pass
                task_file_upload_path = str(dire) + '\\'+str(task_id) + '\\'
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
                task.process_notes.name = remove_absolute_path
                
                task.save()
                max_files.current_files = int(max_files.current_files) + 1
                max_files.save()
            # uploaded_attachment_filename = request.FILES[u'attachment'].name
            # uploaded_attachment_file = request.FILES['attachment']
            # uploaded_attachment_filename = str(task_id) + "/" +  uploaded_attachment_filename
            # task.process_notes.save(uploaded_attachment_filename, uploaded_attachment_file)
            # task.save()
        # print(tasks)
        activities = Activity.objects.all()
        context_data = {
            'tasks': tasks,
            'activities' : activities,
            "error": error,
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
    return HttpResponseRedirect('/partner/tasks')

@login_required
def crud_processed_notes(request):
    if request.method == "POST":
        process_task_id = request.POST.get('process_task_id')
        process_notes_file = request.FILES.get('process_notes_file',False)
        if process_task_id:
            update_file = Task.objects.get(id = process_task_id)
            update_file.process_notes = process_notes_file
            update_file.save()
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
    return HttpResponseRedirect('/partner/tasks')

@login_required
def edit_invoice(request):
    invoice_number_old = request.POST.get('edit_invoice_id')
    audit_plan = AuditPlanMapping.objects.get(invoice_number = invoice_number_old)
    inv_no = request.POST.get('edit_invoice_number')
    amt = request.POST.get('edit_invoice_amount')
    date = request.POST.get('edit_invoice_date')
    ope = request.POST.get('edit_invoice_ope')

    audit_plan.invoice_number = inv_no
    audit_plan.invoice_amount = amt
    audit_plan.invoice_date = date
    audit_plan.out_of_pocket_expenses = ope
    ope_igst = request.POST.get('ope_igst')
    audit_plan.ope_igst = ope_igst

    ope_sgst = request.POST.get('ope_sgst')
    audit_plan.ope_sgst = ope_sgst

    ope_cgst = request.POST.get('ope_cgst')
    total_ope = request.POST.get('total_ope')
    audit_plan.ope_cgst = ope_cgst

    audit_plan.total_ope = total_ope

    igst = request.POST.get('edit_igst')
    sgst = request.POST.get('edit_sgst')
    cgst = request.POST.get('edit_cgst')
    audit_plan.igst = igst
    audit_plan.cgst = cgst
    audit_plan.sgst = sgst
    igsta = request.POST.get('igsta')
    sgsta = request.POST.get('sgsta')
    cgsta = request.POST.get('cgsta')
    audit_plan.igst_amount = igsta
    audit_plan.cgst_amount = cgsta
    audit_plan.sgst_amount = sgsta

    invoice_amount_paid = request.POST.get('invoice_amount_paid')
    invoice_paid_date = request.POST.get('invoice_paid_date')
    is_invoice_paid = request.POST.get('is_invoice_paid')
    if is_invoice_paid == "on":
        print("invoice fully paid")
        invoice_paid = True
    else:
        print("invoice fully not paid")
        invoice_paid = False
    print("invoice paid :",is_invoice_paid,invoice_amount_paid)
    audit_plan.invoice_amount_paid = invoice_amount_paid
    audit_plan.invoice_paid_date = invoice_paid_date
    audit_plan.is_invoice_paid = invoice_paid
    if request.method == "POST":
        try:
            audit_plan.save()
            print("INVOICE CHANGED")
        except Exception as e:
            print("error",e)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

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
        
        return HttpResponseRedirect("/partner/tasks") 

@login_required
def remove_task(request, task_id):
    if task_id:
        task = Task.objects.get(pk = task_id)
        print(task)
        client_tasks = ClientTask.objects.filter(task_name = task.task_name)
        for ct in client_tasks:
            audit_plan_id = ct.auditplan_id
            ap_locked = AuditPlanMapping.objects.get(pk = audit_plan_id)
            if ap_locked.is_audit_plan_locked:
                print("dont delete")
            else:
                ct.delete()
        task.delete()
        return HttpResponseRedirect("/partner/tasks") 

@login_required
def add_client_task(request, client_id):
    if request.method == "POST":
        task_name = request.POST.get('task_name')
        # estimated_days = request.POST.get('estimated_days')
        estimated_hours = request.POST.get('estimated_hours')
        estimated_minutes = request.POST.get('estimated_minutes')
        print(type(estimated_hours) , type(estimated_minutes))
        estimated_hours = int(estimated_hours)
        estimated_minutes = int(estimated_minutes)
        estimated_days = (estimated_hours * 60) + estimated_minutes
        print("total minutes :",estimated_days)
        auditing_standard = request.POST.get('auditing_standard')
        international_auditing_standard = request.POST.get('international_auditing_standard')
        act = request.POST.get('act')
        activity = request.POST.get('activity')
        # audit_type = request.POST.get('audit_type')

        is_there = ClientTask.objects.filter(client__id=client_id).filter(task_name=task_name).exists()
        # print(is_there)
        error = ""
        if is_there:
            error = "Task exists with name: " + str(task_name) 
        else:
            client = Client.objects.get(id=client_id)
            audit_plan = AuditPlanMapping.objects.get(client_id=client_id)
            if audit_plan.is_audit_plan_locked == False:
                newTask = ClientTask(
                    task_name=task_name,
                    task_estimated_days=estimated_days,
                    task_auditing_standard=auditing_standard,
                    task_international_auditing_standard=international_auditing_standard,
                    act=Act.objects.get(id=act),
                    activity=Activity.objects.get(id=activity),
                    client=client,
                    auditplan_id = audit_plan.id
                )
                newTask.save()
        return HttpResponseRedirect(f'/partner/client/{client_id}/profile')
        
        
# ------------------------------------------------End Tasks---------------------------------

# --------------------------------------Clients----------------------------------------
@login_required
def render_client_profile(request, client_id):
    print("yesssss")
    if request.user.is_partner:
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
        acts = Act.objects.all()
        activities = Activity.objects.all()
        audit_type = AuditType.objects.all()
        client = Client.objects.get(id = client_id)
        client_industries = ClientIndustryAuditTypeEntity.objects.values_list('industry_id',flat=True).filter(client=client).distinct()
        client_audittypes = ClientIndustryAuditTypeEntity.objects.values_list('audittype_id',flat=True).filter(client=client).distinct()
        client_entities = ClientIndustryAuditTypeEntity.objects.values_list('entity_id',flat=True).filter(client=client).distinct()
        
        industries = Industry.objects.filter(id__in=client_industries).values_list('industry_name',flat=True)
        entity = Entity.objects.filter(id__in=client_entities).values_list('entity_name',flat=True)
        audittype = AuditType.objects.filter(id__in=client_audittypes).values_list('audit_type_name',flat=True)

        audit_plan = AuditPlanMapping.objects.filter(client_id = client_id)
        
        print(audit_plan)
        ap= AuditPlanMapping.objects.filter(client_id = client_id,is_billable=True)
        total_tasks = 0
        completed_tasks = 0
        is_pending = False
        for a in audit_plan:
            print(a.start_date, a.estimated_end_date , a.actual_end_date)
            total_tasks = ClientTask.objects.filter(auditplan_id = a).count()
            completed_tasks = ClientTask.objects.filter(auditplan_id = a, is_approved_partner = True).count()
            if total_tasks == completed_tasks:
                a.is_pending = True
            else:
                a.is_pending = False
            a.total_tasks = total_tasks
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

        return render(request, 'partner/client_profile.html', context_data)



def render_client_master(request):
    clients = Client.objects.filter(assigned_partner = request.user)
    industries = Industry.objects.all()
    audits = Audits.objects.all()
    entities = Entity.objects.all()
    audittypes = AuditType.objects.all()
    user = User.objects.get(id = request.user.id)
    main_client = User.objects.get(id = user.linked_employee)
    users = User.objects.filter((Q(is_manager = True) & Q(linked_employee = main_client.id))|(Q(is_manager = True) & Q(linked_employee = user.id)))

    ac = Client.objects.filter(assigned_partner_id = request.user.id)
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
    print(client_invoicing,'\n')

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

def client_setup(request):
    if request.method == "GET":
        industries = Industry.objects.all()
        audits = Audits.objects.all()
        entities = Entity.objects.all()
        audittypes = AuditType.objects.all()
        user = User.objects.get(id = request.user.id)
        main_client = User.objects.get(id = user.linked_employee)
        users = User.objects.filter((Q(is_manager = True) & Q(linked_employee = main_client.id))|(Q(is_manager = True) & Q(linked_employee = user.id)))
        partners = User.objects.filter((Q(is_partner = True) & Q(linked_employee = main_client.id))|(Q(is_partner = True) & Q(linked_employee = user.id)))
        context_data = {
            'industries': industries,
            'entities': entities,
            'audittypes': audittypes,
            'users' : users,
            'partners' : partners,
            'audits' : audits
        }
        return render(request, "partner/client_setup.html", context_data)

def add_client(request):
    if request.method == 'POST':
       # print(request)
        clientName = request.POST.get('client_name')
        pan_number = request.POST.get('pan_number')
        tan_number = request.POST.get('tan_number')
        gst_number = request.POST.get('gst_number')
        assigned_user = request.POST.get('assigned_user')
        assigned_partner = request.POST.get('assigned_partner')
        client_email = request.POST.get('client_email')
        finance_email = request.POST.get('finance_email')
        industries_ids = request.POST.getlist('industries')
        audit_type_ids = request.POST.getlist('audit_types')
        entities_ids = request.POST.getlist('entities')
        print("Industries :",industries_ids)
        print("Audit Type :",audit_type_ids)
        print("Entities :",entities_ids)

        user = User.objects.get(pk = assigned_user)
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
                tan_no = tan_number, gst_no = gst_number,
                assigned_user = user,assigned_partner = partner)
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
            # print(activities)
            activities = list(activities)
            # print(activities)
            for activity_id in activities:
                #activity = Activity.objects.get(pk=activity_id)
                tasks = Task.objects.filter(activity_id=activity_id)
                #act = Act.objects.filter(id=activity.act.id)
                # print(tasks)
                # area = Regulator.objects.filter(id=act.area.id)
                for task in tasks:
                    activity = Activity.objects.get(id=task.activity.id)
                    act = Act.objects.get(id=activity.act.id)
                    ClientTask.objects.create(
                        client=client, 
                        task_name=task.task_name,
                        task_estimated_days=task.task_estimated_days,
                        task_auditing_standard=task.task_auditing_standard,
                        task_international_auditing_standard=task.task_international_auditing_standard,
                        activity=activity,
                        act=act,
                        # area_id=act.area.id
                    )

            return HttpResponseRedirect('/partner/clients')

        except Exception as e:
            print(e)
            print("error")
        return HttpResponseRedirect('/partner/clients')

def get_clientdetails(request):
    if request.method == "POST":
        client_id = request.POST.get('client_id')
        client_entities = ClientIndustryAuditTypeEntity.objects.values_list('entity_id').filter(client_id=client_id).distinct()
        client_audittype = ClientIndustryAuditTypeEntity.objects.values_list('audittype_id').filter(client_id=client_id).distinct()
        client_industry = ClientIndustryAuditTypeEntity.objects.values_list('industry_id').filter(client_id=client_id).distinct()
        
        # print(desc)
        client = Client.objects.get(pk=client_id)
        client_name = Client.objects.get(pk=client_id).client_name
        gst = Client.objects.get(pk=client_id).gst_no
        pan = Client.objects.get(pk=client_id).pan_no
        tan = Client.objects.get(pk=client_id).tan_no
        manager = Client.objects.get(pk=client_id).assigned_user_id
        entities = []
        audittype = []
        industries = []
        for entity in client_entities:
            entities.append(entity)

        for audit in client_audittype:
            audittype.append(audit)

        for industry in client_industry:
            industries.append(industry)

        print(entities)
        print(audittype)
        return JsonResponse({'client':client.id,'entities' : entities,'audittype':audittype,'industries':industries,'name':client_name,'gst':gst,'pan':pan,'tan':tan,'manager':manager})

def edit_client(request):
    if request.method == 'POST':
        print("editing")
        clientId = request.POST.get('client_id')
        clientName = request.POST.get('client_name')
        pan_number = request.POST.get('pan_number')
        tan_number = request.POST.get('tan_number')
        gst_number = request.POST.get('gst_number')
        assigned_user = request.POST.get('assigned_user')

        industries_ids = request.POST.getlist('industries')
        audit_type_ids = request.POST.getlist('audit_types')
        entities_ids = request.POST.getlist('entities')

        user = User.objects.get(pk = assigned_user)
        auditplans = AuditPlanMapping.objects.filter(client_id = clientId)
        e = list()
        i = list()
        a = list()

        for z in entities_ids:
            e.append(Entity.objects.get(pk=z))

        for z in industries_ids:
            i.append(Industry.objects.get(pk=z))

        for z in audit_type_ids:
            a.append(AuditType.objects.get(pk=z))

        client = Client.objects.get(pk = clientId)
        clientmap = ClientIndustryAuditTypeEntity.objects.filter(client_id=clientId).delete()
        client.client_name = clientName
        client.pan_no = pan_number
        client.tan_no = tan_number
        client.gst_no = gst_number
        client.assigned_user = user
        client.save()
        # activity.save()
        print(clientmap)
        try:            
            for industry in i:
                for audittype in a:
                    for entity in e:
                        ClientIndustryAuditTypeEntity.objects.create(
                            client = client,
                            audittype = audittype,
                            entity = entity,
                            industry = industry
                        )
            
            print("Add")
            industries_ids = request.POST.getlist('industries')
            audit_type_ids = request.POST.getlist('audit_types')
            entities_ids = request.POST.getlist('entities')

            user = User.objects.get(pk = assigned_user)

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

            
            # print(client)
            

            activities = set()

            # Add to the mapping table
            for industry in industries:
                for audittype in audittypes:
                    for entity in entities:
                        ClientIndustryAuditTypeEntity.objects.get_or_create(
                            client = client,
                            audittype = audittype,
                            entity = entity,
                            industry = industry
                        )
                        activity_objs = ActivityAuditTypeEntity.objects.filter(audittype=audittype, entity=entity, industry=industry)
                        print(activity_objs)
                        for activity_obj in activity_objs:
                            activities.add(activity_obj)
            # Activities
            # print(activities)
            activities = list(activities)
            # print(activities)
            for ap in auditplans:
                if ap.is_audit_plan_locked == 0:
                    for act in activities:
                        if act.audittype_id == ap.audittype_id:
                            print(act.activity_id)

                # print()
                            tasks = Task.objects.filter(activity_id=act.activity_id)
                            print(tasks)
                            for task in tasks:
                                activity = Activity.objects.get(id=task.activity.id)
                                act = Act.objects.get(id=activity.act.id)
                                cnt = ClientTask.objects.filter(task_name = task.task_name,auditplan_id = ap.id).count()
                                print("Default add")
                                if ap.is_audit_plan_locked == 0 and cnt == 0: 
                                    new = ClientTask(
                                                task_name=task.task_name,
                                                task_estimated_days=task.task_estimated_days,
                                                task_auditing_standard=task.task_auditing_standard,
                                                task_international_auditing_standard=task.task_international_auditing_standard,
                                                activity=Activity.objects.get(id=activity.id),
                                                client=client,
                                                act = activity.act,
                                                auditplan_id = ap.id
                                            )
                                    new.save()

            print("check hoga ab")
            ccs = Client.objects.filter(pk = clientId)
            for client in ccs:
                audit_plans = AuditPlanMapping.objects.filter(client_id = client.id)
                print(audit_plans)
                mila = 0
                cts = []
                activity_map = []
                for ap in audit_plans:
                    print(ap.audittype_id)
                    client_details = ClientIndustryAuditTypeEntity.objects.values_list('industry_id','entity_id','audittype_id').filter(client_id = client.id)
                    print(client_details)
                    if ap.is_audit_plan_locked == 0:
                        print("check audit plan")
                        ctss = ClientTask.objects.filter(auditplan_id = ap.id)
                        for ct in ctss:
                            activity_map = ActivityAuditTypeEntity.objects.values_list('industry_id','entity_id','audittype_id').filter(activity_id = ct.activity_id)
                            print(activity_map)
                            for cd in client_details:
                                # print(cd[0])
                                for am in activity_map:
                                    if am[2] == ap.audittype_id:
                                        print("++AUDIT TYPE hau++")
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

            clientmap.save()
        except Exception as e:
            print(e)
    return HttpResponseRedirect('/partner/clients')
def get_tasks(data):
    # Industry : 1-Pharma, 2-Chemical
    # Audit Type: Internal Audit
    # entity: CHS
    

    # temp = []

    # for activity in activities:
    #     for a in activity:
    #         temp.append(a.id)
    # print(temp)

    # Audittypes activities
    audittypes_activities = Activity.objects.filter(audit_type__in=audittypes)#, entities__in=entities).distinct()
    # for a in audittypes_activities:
    #     activities.add(a)       
    # print(activities)

    # tasks = Task.objects.filter(activity__in=activities)
    tasks = None
    # acts = Act.objects.filter(Q(industry__in=industries)).distinct()
    if settings.DEBUG:
        print(industries)
        print(audittypes)
        print(entities)
        # tasks = Task.objects.filter(activity__act__industry__in = industries)
        print(tasks)
        # print(activities)
    return tasks, activities

    # Task: Task.objects.filter(activity__act__industry = industries,activity__audity_type =  )
    # if type_of_data == 'industry':
    #     acts = Act.objects.filter(industry__in=data)
    #     activities = Activity.objects.filter(act__in=acts)
    #     tasks = Task.objects.filter(activity__in=activities)
    #     print(activities)
    #     print(tasks)
    #     return tasks, activities
    # elif type_of_data == 'audit_type':
    #     activities = Activity.objects.filter(audit_type__in=data)
    #     tasks = Task.objects.filter(activity__in=activities)
    #     print(activities)
    #     print(tasks)
    #     return tasks, activities
    # else:
    #     activities = Activity.objects.filter(entities__in=data)
    #     tasks = Task.objects.filter(activity__in=activities)
    #     print(activities)
    #     print(tasks)
    #     return tasks, activities
    

def remove_client(request,client_id):
    if client_id:
        client = Client.objects.filter(pk=client_id)
        client.delete()
        return HttpResponseRedirect('/partner')               

def view_client_activitiess(request, client_id):
    if request.method == 'GET':
        users = User.objects.exclude(username__startswith="admin")
        
        # Client
        client = Client.objects.get(pk = client_id)

        # Client industry
        client_industry = client.industry
        business_client_industry = client.industry
        finance_client_industry=client.industry

        # Act industry
        acts = Act.objects.filter(industry = client_industry)
        
        #Business  Area industry
        business_area = Area.objects.filter(industry = business_client_industry)
        
        #Finance  Area industry
        finance_area = F_Area.objects.filter(f_industry=finance_client_industry)
        
        # Dump all activities as tasks
        activities = []
        areas = []
        f_areas=[]
        for act in acts:
            activities.append(Activity.objects.filter(act = act))
            
        #print(activities)
        #print(areas)
        
        
        context = {
            'activities': activities,
            'areas':areas,
            'f_areas':f_areas,
            'users':users,
            'client_id': client_id
        }

        return render(request, 'partner/client_profile.html', context)

def assign_task_to_employee(request,client_id):
    print("assigning")
    if request.method == 'POST':
        activityName = request.POST.get('activity_name')
        user_id = request.POST.get('username')
        task_relevance = request.POST.get('task_relevance')
        volume = request.POST.get('volume')
        samplerate = request.POST.get('samplerate')
        act = request.POST.get('activity_act')
        regulation = request.POST.get('activity_regulation')
        user = User.objects.get(pk = user_id)
        client_id = request.POST.get('client_id')
        print(client_id)
        client = Client.objects.get(pk = client_id)
        try:

            # newTask = AssignedActivities(activity_name=activityName, activity_description=activityDescription, task_start_date=startDate, task_end_date=endDate,user=user)
            # newTask.save()
            print(user)
            task = Task(user=user,task_relevance=task_relevance,task_sample_rate=samplerate,task_volume=volume)
            task.save()
            # Deliver email to the assigned user
            user_email = user.email
            if user_email is not None:
                msg = """Hello %s !!!
                    # I have assigned you a Task. Take a look at this.
                    #Following is the Task deails......"""
                send_mail("Task Assignment", msg, 'icraftsolution.com@gmail.com',[user_email], fail_silently=False)
        except Exception as e:
            print(e)
        return HttpResponseRedirect("/manager/client/{}/tasks".format(client_id)) 
    return HttpResponseRedirect("/manager/tasks") 

# Clone Clients 
def clone_client(request):
    if request.method == "POST":
        client_id = request.POST.get('clone_client_id')
        client_name = request.POST.get('clone_client_name')
        client_industry_id = request.POST.get('clone_client_industry')
        # Get all the tasks of the exisiting client
        tasks = Task.objects.filter(client__id = client_id)

        industry = Industry.objects.get(pk = client_industry_id)

        try:
            newClient = Client(client_name = client_name, industry = industry)
            newClient.save()

            for task in tasks:
                # print(task)
                newTask = Task(task_name=task.task_name, task_regulation_name=task.task_regulation_name, task_act_name=task.task_act_name, task_activity_name=task.task_activity_name, task_start_date=task.task_start_date, task_end_date=task.task_end_date, client=newClient)
                newTask.save()
                # print(newTask)
            print("All Tasks Added")
                
        except Exception as e:
            print(e)
            pass   

        return HttpResponseRedirect('/partner/')


def get_client_tasks(type_of_data, data, client_id):
    if type_of_data == 'industry':
        acts = Act.objects.filter(industry__in=data)
        activities = Activity.objects.filter(act__in=acts).distinct()
        tasks = ClientTask.objects.filter(client__id=client_id).filter(activity__in=activities).distinct()
        # print(tasks)
        return tasks
    elif type_of_data == 'audit_type':
        activities = Activity.objects.filter(audit_type__in=data).distinct()
        tasks = ClientTask.objects.filter(client__id=client_id).filter(activity__in=activities).distinct()
        # print(activities)
        # print(tasks)
        return tasks
    else:
        activities = Activity.objects.filter(entities__in=data).distinct()
        tasks = ClientTask.objects.filter(client__id=client_id).filter(activity__in=activities).distinct()
        # print(activities)
        # print(tasks)
        return tasks

def list_clients_setup(request):
    clients = Client.objects.all()
    tasks = Task.objects.all()
    users=User.objects.all()
    context={

        'clients':clients,
        'tasks':tasks,
        'users':users
        
    }
    return render(request,"partner/assign_clients_steup_lists.htm",context)

@login_required
def employee_setup(request):
    if request.user.is_authenticated:
        linked_employee = request.user.linked_employee
        users = User.objects.filter(Q(linked_employee = linked_employee) | Q(linked_employee = request.user.id))
        print(users)
        
    context={
        'users':users
        
    }
    return render(request,"partner/employee_setup.html",context) 

@login_required
def add_employee(request):
    if request.method == "POST":
        employee_fname = request.POST.get('employee_fname')
        employee_lname = request.POST.get('employee_lname')
        employee_username = request.POST.get('employee_username')
        employee_password = request.POST.get('employee_password')
        employee_email = request.POST.get('employee_email')
        role = request.POST.get('role')    
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
                        linked_employee=request.user.id
                    )
                elif role == "manager":
                    new_user = User(username=employee_username, 
                        first_name=employee_fname, 
                        last_name=employee_lname,
                        is_manager=True,
                        email = employee_email,
                        password = make_password(employee_password),
                        linked_employee=request.user.id
                    )
                    
                elif role == "auditor":
                    new_user = User(username=employee_username, 
                        first_name=employee_fname, 
                        last_name=employee_lname,
                        is_auditorclerk=True,
                        email = employee_email,
                        password = make_password(employee_password),
                        linked_employee=request.user.id
                    )
                elif role == "article":
                    new_user = User(username=employee_username, 
                        first_name=employee_fname, 
                        last_name=employee_lname,
                        is_articleholder=True,
                        email = employee_email,
                        password = make_password(employee_password),
                        linked_employee=request.user.id
                    )
                if new_user is not None:
                    print("new user saved")
                    user = User.objects.get(id = request.user.id)
                    print("user logged in",user)
                    if user.linked_employee == "":
                        print("null")
                    else:
                        main_client = User.objects.get(id=user.linked_employee)
                        # print(main_client)
                        add_user_count = MaxUsers.objects.get(main_client = main_client.id)
                        if add_user_count.max_users == add_user_count.current_users:
                            error = "limit of user creation exceeded. You Cannot add more users !!"
                        else:
                            print("user added successfully..!")
                            add_user_count.current_users = int(add_user_count.current_users) + 1
                            add_user_count.save()
                            new_user.save()
                    # new_user.save()
                    get_latest_user = User.objects.latest('id')
                
        
        linked_employee = request.user.linked_employee
        employees = User.objects.filter(Q(linked_employee = linked_employee) | Q(linked_employee = request.user.id))
        context_data = {
            "error": error,
            "users": employees
        }
        return render(request, "partner/employee_setup.html", context_data)
        # return HttpResponseRedirect("/partner/employee/setup") 

@login_required
def edit_employee(request):
    if request.method == 'POST':
        userId = request.POST.get('user_id')
        newPassword = request.POST.get('new_password')
        
        user = User.objects.get(pk = userId)
        user.password = make_password(newPassword)
        try:
            user.save()
        except Exception as e:
            print(e)
        
        return HttpResponseRedirect("/partner/employee/setup") 

# -------------------------------End Client---------------------------------

# -------------------------------Audit Plan---------------------------------
@login_required
def audit_plan(request, auditplan_id):
    print("yes this page :",auditplan_id)
    auditplan = AuditPlanMapping.objects.get(id=auditplan_id)
    # print("AUDIT PLANS:\n",auditplan)
    client_tasks = ClientTask.objects.filter(auditplan_id=auditplan.id)
    # print(client_tasks)
    labels = Activity_Labels.objects.values('activity_label_name')
    client_audittype = ClientIndustryAuditTypeEntity.objects.values_list('audittype_id').filter(client_id=auditplan.client_id).distinct()
    manager = Client.objects.values_list('assigned_user_id').filter(pk=auditplan.client_id)
    test = ClientIndustryAuditTypeEntity.objects.values('audittype_id').filter(client_id=auditplan.client_id).distinct()
    ids = []
    for r in test:
        ids.append(r['audittype_id'])
    mng = ""
    for m in manager:
        emp = User.objects.filter(pk=m[0])
    mng = emp[0]
    # print("=====",mng,"=====")
    ap = []
    ac = []
    for ca in ids:
        ap.append(ActivityAuditTypeEntity.objects.values_list('activity_id',flat=True).filter(audittype_id = ca).distinct())
        ac = ActivityAuditTypeEntity.objects.filter(audittype_id = ca).distinct()
    audittypes = AuditType.objects.filter(pk = auditplan.audittype_id)
    print(ap)
    tlist = []
    j=0
    print(len(ap))
        
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
            
        
        obj = {
            "tasks": task,
            "partner_upload":partner_attachment_file,
            "manager_upload":manager_attachment_file,
            "auditor_upload":auditor_attachment_file,
            "article_upload":article_attachment_file,
            "estimated_time":str(int(task.task_estimated_days)  // 60) + ":" + str(int(task.task_estimated_days)  % 60)
            
        }
        client_tasks_list.append(obj)
    # for ct in client_tasks:
    #     print(type(ct.task_estimated_days))
        # te = int(ct.task_estimated_days)
        # estimated_time = estimated_time + te
    print(client_tasks)
    print(client_tasks_list)

    # print(estimated_time)
    # print("=====TIME AVAILABLE=======")
    time_available = auditplan.estimated_end_date - auditplan.start_date
    buffer = auditplan.actual_end_date - auditplan.estimated_end_date
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
        'manager' : mng,
        'audit_plan' : auditplan,
        'looptimes' : looptimes,
        'time_available' : ta,
        'buffer' : buff,
        # 'industries_activities': industries_activities
    }
    return render(request, 'partner/audit_plan.html', context_data)

@login_required
def add_audit_plan(request,client_id):
    print(client_id)
    if request.method == "POST":
        audit_plan_name = request.POST.get('audit_plan_name')
        auditplan_startdate = request.POST.get('auditplan_startdate')
        auditplan_enddate = request.POST.get('auditplan_enddate')
        auditplan_actual_enddate = request.POST.get('auditplan_actual_enddate')
        auditplan_frequency = request.POST.get('auditplan_frequency')
        auditplan_fy = request.POST.get('auditplan_fy')
        auditplan_ap = request.POST.get('auditplan_ap')
        is_billable = request.POST.get('is_billable')
        
        if is_billable is None:
            is_billable = False
        auditplan = AuditPlanMapping(auditplanname=audit_plan_name, start_date=auditplan_startdate,
                                     estimated_end_date=auditplan_enddate, actual_end_date=auditplan_actual_enddate,
                                     auditplan_frequency=auditplan_frequency, finance_year=auditplan_fy,
                                     client_id=client_id, audittype_id=auditplan_ap, is_billable=is_billable)
        # print(auditplan_startdate)
        try:
            auditplan.save()
            print("auditplan saved successfully :",auditplan_startdate, auditplan_enddate, auditplan_actual_enddate)
        except Exception as e:
            raise e
        
        auditplan = AuditPlanMapping.objects.all().last()
        industries = ClientIndustryAuditTypeEntity.objects.values_list('industry_id').filter(client_id=auditplan.client_id)
        entities = ClientIndustryAuditTypeEntity.objects.values_list('entity_id').filter(client_id=auditplan.client_id)
        # audittypes = ClientIndustryAuditTypeEntity.objects.values_list('audittype_id').filter(client_id=auditplan.client_id)
        print(industries,entities)
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

    return HttpResponseRedirect(f'/partner/client/{client_id}/profile')

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
        return HttpResponseRedirect(f'/partner/client/auditplan/{audit_plan.id}',{'msg' : "msg"})

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
    return HttpResponseRedirect(f'/partner/client/auditplan/{audit_plan.id}',{'msg' : msg})

@login_required
def mapping(request):
    tasks = Task.objects.all()
    auditmappings = ActivityAuditTypeEntity.objects.all()
    activities = Activity.objects.all()
    audit_types = AuditType.objects.all()
    entities = Entity.objects.all()
    industries = Industry.objects.all()    
    context_set={
        'tasks' : tasks,
        'auditmappings' : auditmappings,
        'activities': activities,
        'audittypes': audit_types,
        'entities': entities,
        'industries': industries,
    }
    return render(request, 'partner/mapping.html', context_set)

@login_required
def partner_approval_pending_tasks(request):
    if request.user.is_partner:
        # main_client = User.objects.get(id = request.user.linked_employee)
        client_tasks = []
        clients = Client.objects.filter(assigned_partner = request.user)
        for client in clients:
            get_client_tasks = ClientTask.objects.filter(Q(client = client) & Q(status=True) & Q(is_start=True) & Q(is_approved_partner=False))
            for clienttasks in get_client_tasks:
                client_tasks.append(clienttasks)

        # waiting_approvals = ClientTask.objects.filter(status=True,is_start=True,is_approved_partner=False)
        context={
            'waiting_approvals':client_tasks
        }
        return render(request, "partner/waiting_approvals.html", context)

@login_required 
def Reports(request):
    if request.user.is_partner:
        if request.method == 'POST':
            user_id = request.POST.get('user_id')
            toggle = request.POST.get('toggle')
            if user_id and toggle:
                user = User.objects.get(id = user_id)
                get_client = Client.objects.filter(assigned_partner=user)
                client_tasks = []
                if toggle == "completed":
                    for client in get_client:
                        get_client_tasks = ClientTask.objects.filter(Q(client=client) & Q(is_approved_partner=True))
                        in_time =  False
                        data = []
                        estimated_end_date = None
                        
                        for task in get_client_tasks:
                            if task.task_start_datetime is not None and task.task_end_datetime is not None:
                                task_start_datetime = task.task_start_datetime.strftime("%d-%m-%Y %H:%M:%S")
                                task_end_datetime = task.task_end_datetime.strftime("%d-%m-%Y %H:%M:%S")
                                estimated_end_date = task.task_start_datetime + timedelta(minutes = int(task.task_estimated_days))
                                estimated_datetime = estimated_end_date.strftime("%d-%m-%Y %H:%M:%S")
                                # print("result 4 :",estimated_end_date , int(task.task_estimated_days))
                                in_time = True

                                if estimated_end_date < task.task_end_datetime:
                                    in_time = False   
                            else:
                                if task.task_start_datetime:
                                    task_start_datetime = task.task_start_datetime.strftime("%d-%m-%Y %H:%M:%S")
                                    estimated_datetime = (task.task_start_datetime + timedelta(minutes = int(task.task_estimated_days))).strftime("%d-%m-%Y %H:%M:%S")
                                else:
                                    task_start_datetime = "Not Started"
                                    estimated_datetime = ""
                                if task.task_end_datetime:
                                    task_end_datetime = task.task_end_datetime.strftime("%d-%m-%Y %H:%M:%S")
                                else:
                                    task_end_datetime = "Not Completed" 
                            # print(task.task_start_datetime.strftime("%Y-%m-%d %H:%M:%S"),task.task_end_datetime.strftime("%Y-%m-%d %H:%M:%S"),estimated_end_date.strftime("%Y-%m-%d %H:%M:%S"),in_time)
                            partner_file_location = ""
                            manager_file_location = ""
                            auditor_file_location = ""
                            article_file_location = ""
                            if task.partner_attachment_file: 
                                print("yes")
                                str_data = task.partner_attachment_file.replace("'",'"')
                                json_data = json.loads(str_data)
                                partner_file_location = json_data['file_location']
                            if task.manager_attachment_file: 
                                print("Manager :",task.manager_attachment_file)
                                str_data = task.manager_attachment_file.replace("'",'"')
                                json_data = json.loads(str_data)
                                manager_file_location = json_data['file_location']
                            if task.auditor_attachment_file: 
                                str_data = task.auditor_attachment_file.replace("'",'"')
                                json_data = json.loads(str_data)
                                auditor_file_location = json_data['file_location']
                            if task.article_attachment_file: 
                                str_data = task.article_attachment_file.replace("'",'"')
                                json_data = json.loads(str_data)
                                article_file_location = json_data['file_location']
                            obj = {
                                'task_name':task.task_name,
                                "is_approved_partner":task.is_approved_partner,
                                'task_start_datetime':task_start_datetime,
                                'estimated_end_date': estimated_datetime,
                                'task_end_datetime':task_end_datetime,
                                'in_time':in_time,
                                "partner_file_location":partner_file_location,
                                "manager_file_location":manager_file_location,
                                "auditor_file_location":auditor_file_location,
                                "article_file_location":article_file_location
                            }
                            data.append(obj)
                        
                        return JsonResponse({'data':data})
                elif toggle == "pending":
                    for client in get_client:
                        get_client_tasks = ClientTask.objects.filter(Q(client=client) & Q(is_approved_partner=False))
                        in_time =  False
                        data = []
                        estimated_end_date = None
                        
                        for task in get_client_tasks:
                            # print("start datetime : ",task.task_start_datetime)
                            # print("end datetime : ",task.task_end_datetime)
                            if task.task_start_datetime is not None and task.task_end_datetime is not None:
                                task_start_datetime = task.task_start_datetime.strftime("%d-%m-%Y %H:%M:%S")
                                task_end_datetime = task.task_end_datetime.strftime("%d-%m-%Y %H:%M:%S")
                                estimated_end_date = task.task_start_datetime + timedelta(minutes = int(task.task_estimated_days))
                                # print("result 4 :",estimated_end_date , int(task.task_estimated_days))
                                estimated_datetime = estimated_end_date.strftime("%d-%m-%Y %H:%M:%S")
                                in_time = True

                                if estimated_end_date < task.task_end_datetime:
                                    in_time = False   
                            else:
                                if task.task_start_datetime:
                                    task_start_datetime = task.task_start_datetime.strftime("%d-%m-%Y %H:%M:%S")
                                    estimated_datetime = (task.task_start_datetime + timedelta(minutes = int(task.task_estimated_days))).strftime("%d-%m-%Y %H:%M:%S")
                                else:
                                    task_start_datetime = "Not Started"
                                    estimated_datetime = ""
                                if task.task_end_datetime:
                                    task_end_datetime = task.task_end_datetime.strftime("%d-%m-%Y %H:%M:%S")
                                else:
                                    task_end_datetime = "Not Completed"
                                
                            # print(task.task_start_datetime.strftime("%Y-%m-%d %H:%M:%S"),task.task_end_datetime.strftime("%Y-%m-%d %H:%M:%S"),estimated_end_date.strftime("%Y-%m-%d %H:%M:%S"),in_time)
                            partner_file_location = ""
                            manager_file_location = ""
                            auditor_file_location = ""
                            article_file_location = ""
                            if task.partner_attachment_file: 
                                str_data = task.partner_attachment_file.replace("'",'"')
                                json_data = json.loads(str_data)
                                partner_file_location = json_data['file_location']
                            if task.manager_attachment_file: 
                                str_data = task.manager_attachment_file.replace("'",'"')
                                json_data = json.loads(str_data)
                                manager_file_location = json_data['file_location']
                            if task.auditor_attachment_file: 
                                str_data = task.auditor_attachment_file.replace("'",'"')
                                json_data = json.loads(str_data)
                                auditor_file_location = json_data['file_location']
                            if task.article_attachment_file: 
                                str_data = task.article_attachment_file.replace("'",'"')
                                json_data = json.loads(str_data)
                                article_file_location = json_data['file_location']
                            obj = {
                                'task_name':task.task_name,
                                "is_approved_partner":task.is_approved_partner,
                                'task_start_datetime':task_start_datetime,
                                'estimated_end_date': estimated_datetime,
                                'task_end_datetime':task_end_datetime,
                                'in_time':in_time,
                                "partner_file_location":partner_file_location,
                                "manager_file_location":manager_file_location,
                                "auditor_file_location":auditor_file_location,
                                "article_file_location":article_file_location
                            }
                            data.append(obj)
                        
                        return JsonResponse({'data':data})
                           
                if toggle == "rejected":
                    for client in get_client:
                        get_client_tasks = ClientTask.objects.filter(Q(client=client) & Q(is_rejected=True))
                        in_time =  False
                        data = []
                        estimated_end_date = None
                        
                        for task in get_client_tasks:
                            if task.task_start_datetime is not None and task.task_end_datetime is not None:

                                estimated_end_date = task.task_start_datetime + timedelta(minutes = int(task.task_estimated_days))
                                # print("result 4 :",estimated_end_date , int(task.task_estimated_days))
                                in_time = True

                                if estimated_end_date < task.task_end_datetime:
                                    in_time = False    
                            # print(task.task_start_datetime.strftime("%Y-%m-%d %H:%M:%S"),task.task_end_datetime.strftime("%Y-%m-%d %H:%M:%S"),estimated_end_date.strftime("%Y-%m-%d %H:%M:%S"),in_time)
                            partner_file_location = ""
                            manager_file_location = ""
                            auditor_file_location = ""
                            article_file_location = ""
                            if task.partner_attachment_file: 
                                str_data = task.partner_attachment_file.replace("'",'"')
                                json_data = json.loads(str_data)
                                partner_file_location = json_data['file_location']
                            if task.manager_attachment_file: 
                                str_data = task.manager_attachment_file.replace("'",'"')
                                json_data = json.loads(str_data)
                                manager_file_location = json_data['file_location']
                            if task.auditor_attachment_file: 
                                str_data = task.auditor_attachment_file.replace("'",'"')
                                json_data = json.loads(str_data)
                                auditor_file_location = json_data['file_location']
                            if task.article_attachment_file: 
                                str_data = task.article_attachment_file.replace("'",'"')
                                json_data = json.loads(str_data)
                                article_file_location = json_data['file_location']
                            
                            obj = {

                                'task_name':task.task_name,
                                "is_rejected":task.is_rejected,
                                'task_start_datetime':task.task_start_datetime.strftime("%d-%m-%Y %H:%M:%S"),
                                'estimated_end_date': estimated_end_date.strftime("%d-%m-%Y %H:%M:%S"),
                                'task_end_datetime':task.task_end_datetime.strftime("%d-%m-%Y %H:%M:%S"),
                                'in_time':in_time,
                                "partner_file_location":partner_file_location,
                                "manager_file_location":manager_file_location,
                                "auditor_file_location":auditor_file_location,
                                "article_file_location":article_file_location
                                
                            }
                            data.append(obj)
                        
                        return JsonResponse({'data':data})
                # in_time =  False
                # data = []
                # estimated_end_date = None
                
                # for task in client_tasks:
                #     if task.task_start_datetime is not None and task.task_end_datetime is not None:

                #         estimated_end_date = task.task_start_datetime + timedelta(minutes = int(task.task_estimated_days))
                #         # print("result 4 :",estimated_end_date , int(task.task_estimated_days))
                #         in_time = True

                #         if estimated_end_date < task.task_end_datetime:
                #             in_time = False    
                #     # print(task.task_start_datetime.strftime("%Y-%m-%d %H:%M:%S"),task.task_end_datetime.strftime("%Y-%m-%d %H:%M:%S"),estimated_end_date.strftime("%Y-%m-%d %H:%M:%S"),in_time)
                #     obj = {
                #         'task_name':task.task_name,
                #         "is_approved_partner":task.is_approved_partner,
                #         'task_start_datetime':task.task_start_datetime.strftime("%d-%m-%Y %H:%M:%S"),
                #         'estimated_end_date': estimated_end_date.strftime("%d-%m-%Y %H:%M:%S"),
                #         'task_end_datetime':task.task_end_datetime.strftime("%d-%m-%Y %H:%M:%S"),
                #         'in_time':in_time
                #     }
                #     data.append(obj)
                # clienttaskserializer = ClientTaskSerializer(client_tasks,many=True)
                # return JsonResponse({'data':data})
                
        return render(request, "partner/reports.html")

@login_required 
def pending_approval_task(request, task_id):
    print("yes")
    if request.user.is_partner:
        task = ClientTask.objects.get(id = task_id)
        client = Client.objects.get(id = task.client_id)
        estimated_end_date = None
        in_time = False
        if task.task_start_datetime is not None and task.task_end_datetime is not None:
            
            # estimated_end_date = 5
            # print(task.id,task.task_start_date,task.task_estimated_days)

            # ✅ parse datetime string and add minutes to datetime

            
           

            estimated_end_date = task.task_start_datetime + timedelta(minutes = int(task.task_estimated_days))
            print("result 4 :",estimated_end_date , int(task.task_estimated_days))
            in_time = True

            if estimated_end_date < task.task_end_datetime:
                in_time = False
        manager_file_location = ""
        if task.manager_attachment_file: 
            str_data = task.manager_attachment_file.replace("'",'"')
            json_data = json.loads(str_data)
            manager_file_location = json_data['file_location']
        print(in_time)
        context_data = {
            'task': task, 
            'client': client,
            "manager_file_location":manager_file_location,
            'estimated_end_date': estimated_end_date,
            "estimated_time":str(int(task.task_estimated_days)  // 60) + ":" + str(int(task.task_estimated_days)  % 60),
            'in_time': in_time
        }
        return render(request, "partner/task_approval_page.html", context_data)

@login_required
def approve_tasks(request,task_id):
    if request.user.is_partner:
        try:
            getuser = User.objects.get(id=request.user.id)
            print(getuser)
        except User.DoesNotExist:
            getuser = "none"
        if request.method == "POST":      
            feedback = request.POST.get('feedback')      
            print(feedback)
            task = ClientTask.objects.get(id = task_id)
            task.partner_feedback = feedback

            attachment = request.FILES.get('attachment', False)
            print(attachment)
            if attachment:
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
                            task_file_upload_path = str(dire) + '\\'+str(task_id) + '\\' + 'partner' +'\\'
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
                            # task.partner_attachment_file.name = remove_absolute_path
                            
                            task.partner_attachment_file =  {
                                "user_id":f"{request.user.id}",
                                "file_location":f"{remove_absolute_path}"
                            }
                            
                            get_max_files.current_files = int(get_max_files.current_files) + 1
                            get_max_files.save()
                    except MaxFiles.DoesNotExist:
                        print("no max files found")
                    
                task.status = True
                # task.save()

            # if attachment:
            #     uploaded_attachment_filename = request.FILES[u'attachment'].name
            #     uploaded_attachment_file = request.FILES['attachment']
            #     uploaded_attachment_filename = str(task_id) + "/" +  uploaded_attachment_filename
            #     # print(uploaded_attachment_filename)
                
            #     task.partner_attachment_file.save(uploaded_attachment_filename, uploaded_attachment_file)
            #     # task.attachment_file = request.FILES['attachment']
            #     task.status = True
            #     task.save()

        task.is_approved_partner = True                                                                             
        print(task)
        task.task_end_date = date.today()
        task.save()
        print(task.partner_attachment_file)
        return HttpResponseRedirect(f'/partner/approval/{task_id}')

@login_required
def reject_task(request,task_id):
    if request.user.is_partner:
        remark_data = request.POST.get('remark')
        task = ClientTask.objects.get(id=task_id)
        task.reject_task_remark=remark_data
        task.is_rejected = True
        task.status = False
        task.is_start = False
        task.save()
        return HttpResponseRedirect(f'/partner/approval/{task_id}')

def partner_list_of_clients(request):
    if request.user.is_partner: 
        # clients = Client.objects.filter(assigned_user=request.user.id)
        clients = Client.objects.filter(assigned_partner = request.user)
        
        context = {
            "clients":clients
        }
        return render(request,"partner/list_of_clients.html",context)

def partner_client_tasks(request,client_id):
    if request.user.is_partner:
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
        user = User.objects.filter(id = request.user.linked_employee)
        for i in user:
            sub_user = User.objects.filter(linked_employee = i.id)
            for j in sub_user:
                users.append(j)
        tasks_of_client = ClientTask.objects.filter(client_id=client_id)
        reassign_tasks = ClientTask.objects.filter(client_id=client_id,is_reject=True)
        
        context= {
            'client': client,
            'tasks': tasks_of_client,
            "users": users,
            'reassign_tasks': reassign_tasks,
            'industry': industries,
            'audittype': audittype,
            'entity' : entity,
        }

        return render(request,"partner/client_tasks.html",context)
@login_required
def partner_client_task(request):
    tasks = ClientTask.objects.filter(user = None)
    users = User.objects.exclude(is_partner=True).exclude(is_manager=True).exclude(is_admin=True)
    context_data={
        'tasks': tasks,  
        'users': users
    }
    return render(request,'partner/assign_task_master.html',{})

@login_required
def partner_assign_task_to_employee(request, client_id):
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
        return HttpResponseRedirect(f"/partner/client/{client_id}/tasks/")

def partner_tasks(request):
    if request.user.is_partner:
        current_user = request.user
        assigned_tasks = ClientTask.objects.filter(user=current_user.id).filter(is_approved=False,is_reject=False,is_rejected=False,status=False)
        # print(assigned_activities)
        context_data = {
            'tasks': assigned_tasks
        }
        return render(request, "partner/partner_tasks.html", context_data)

@login_required
def show_individual_partner_task(request, task_id):
    if request.user.is_partner:
        task = ClientTask.objects.get(id = task_id)
        client = Client.objects.get(id = task.client_id)
    
        estimated_end_date = None
        in_time = False
        if task.task_start_datetime is not None and task.task_end_datetime is not None:
            estimated_end_date = task.task_start_datetime + timedelta(minutes = int(task.task_estimated_days))
            in_time = True

            if estimated_end_date < task.task_end_datetime:
                in_time = False
        file_location = ""
        if task.partner_attachment_file: 
            str_data = task.partner_attachment_file.replace("'",'"')
            json_data = json.loads(str_data)
            file_location = json_data['file_location']
        print(estimated_end_date)
        context_data = {
            'task': task, 
            'client': client,
            'estimated_end_date': estimated_end_date,
            'in_time': in_time,
            'file_location':file_location,
            "estimated_time":str(int(task.task_estimated_days)  // 60) + ":" + str(int(task.task_estimated_days)  % 60)
        }
        return render(request, 'partner/individual_task.html', context_data)

@login_required
def partner_start_working(request,task_id):
    if request.user.is_partner:
        task= ClientTask.objects.filter(id=task_id).update(is_start=True,task_start_date=date.today(),task_start_datetime=datetime.now(),is_rejected = False)
        print(task)
    return HttpResponseRedirect('/partner/my_task/{}'.format(task_id))

@login_required
def partner_task_submission(request, task_id):
    if request.user.is_partner:
        if request.method == "POST":            
            feedback = request.POST.get('feedback')      
            print(feedback)
            try:
                getuser = User.objects.get(id=request.user.id)
                print(getuser)
            except User.DoesNotExist:
                getuser = "none"
            task = ClientTask.objects.get(id = task_id)
            task.partner_feedback = feedback
            task.is_approved_partner = True
            attachment = request.FILES.get('attachment', False)
            print(attachment)
            if attachment:
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
                            task_file_upload_path = str(dire) + '\\'+str(task_id) + '\\' + 'partner' +'\\'
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

            #     task.partner_attachment_file.save(uploaded_attachment_filename, uploaded_attachment_file)
            #     # task.attachment_file = request.FILES['attachment']
            #     task.remark = request.POST.get('remark')
            task.remark = request.POST.get('remark')
            task.task_end_datetime = datetime.now()
            task.status = True
            task.save()
        return HttpResponseRedirect('/partner/my_task/{}'.format(task_id))

@login_required
def view_client_invoicing(request,client_id):
    audit_plans = AuditPlanMapping.objects.filter(client_id = client_id,is_billable=True)
    client = Client.objects.filter(id = client_id)
    print(client[0])
    ap = []
    for a in audit_plans:
        if a.invoice_number is not None:
            ap.append(a)
    # print(client)
    for c in client:
        print(c)
    return render(request, "partner/client_invoice.html", {'audit_plans':ap,'client':client[0]})

@login_required
def client_invoice_download(request,auditplan_id):
    if request.method == "POST":
        print(request.FILES.get("file"))
    print(auditplan_id)
    audit_plan = AuditPlanMapping.objects.get(id = auditplan_id)
    print(audit_plan)
    if audit_plan.igst_amount:
        igst = audit_plan.igst_amount
    else:
        igst = 0
    if audit_plan.sgst_amount:
        sgst = audit_plan.sgst_amount
    else:
        sgst = 0
    if audit_plan.cgst_amount:
        cgst = audit_plan.cgst_amount
    else:
        cgst = 0
    total_gst = int(igst) + int(sgst) + int(cgst)
    obj = {
        'client':audit_plan.client, 
        'client_email':audit_plan.client.client_email,
        'invoice_amount' : audit_plan.invoice_amount,
        'invoice_number':audit_plan.invoice_number,
        'invoice_date' : audit_plan.invoice_date,
        'ope':audit_plan.out_of_pocket_expenses,
        'igst':audit_plan.igst,
        'sgst':audit_plan.sgst,
        'cgst':audit_plan.cgst,
        'igsta':audit_plan.igst_amount,
        'sgsta':audit_plan.sgst_amount,
        'cgsta':audit_plan.cgst_amount,
        'total_gst':total_gst,
        'ope_igst':audit_plan.ope_igst,
        'ope_sgst':audit_plan.ope_sgst,
        'ope_cgst':audit_plan.ope_cgst,
        'total_ope':audit_plan.total_ope,
        'invoice_paid_date':audit_plan.invoice_paid_date,
        'invoice_amount_paid':audit_plan.invoice_amount_paid,
        'is_invoice_paid':audit_plan.is_invoice_paid,  
    }
    params = {
        "obj":obj,
        'url':audit_plan.id
    }
    return render(request,"partner/invoice_download.html",params)


@login_required
def create_invoice(request,client_id):
    if request.method == "POST":
        ap =  request.POST.get('auditplan_ap')
        audit_plan = AuditPlanMapping.objects.get(pk=ap,is_billable=True)
        print(audit_plan)
        invoice_number = request.POST.get('invoice_number')
        invoice_date = request.POST.get('invoice_date')
        invoice_amount = request.POST.get('invoice_amount')
        
        
        audit_plan.invoice_number = invoice_number
        audit_plan.invoice_date = invoice_date
        audit_plan.invoice_amount = invoice_amount
        
        out_of_pocket = request.POST.get('out_of_pocket')
        ope_igst = request.POST.get('ope_igst')
        total_ope = request.POST.get('total_ope')
        audit_plan.out_of_pocket_expenses = out_of_pocket
        audit_plan.ope_igst = ope_igst
        audit_plan.total_ope = total_ope

        ope_sgst = request.POST.get('ope_sgst')
        audit_plan.ope_sgst = ope_sgst

        ope_cgst = request.POST.get('ope_cgst')
        audit_plan.ope_cgst = ope_cgst

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
        try:
            audit_plan.save()
            print("saved")
        except Exception as e:
            print("error :",e)
            
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def invoice_details(request):
    if request.method == "POST":
        invoice_number = request.POST.get('invoice_number')
        invoice_details = AuditPlanMapping.objects.get(invoice_number = invoice_number)
        print("is_invoice_paid = ",invoice_details.is_invoice_paid)
        invoices = AuditPlanMapping.objects.filter(invoice_number = invoice_number)
        data = []
        for i in invoices:
            data.append(i.id)
        print(data)
        return JsonResponse({
            'invoice_amount' : invoice_details.invoice_amount,
            'invoice_number':invoice_details.invoice_number,
            'invoice_date' : invoice_details.invoice_date,
            'ope':invoice_details.out_of_pocket_expenses,
            'igst':invoice_details.igst,
            'sgst':invoice_details.sgst,
            'cgst':invoice_details.cgst,
            'igsta':invoice_details.igst_amount,
            'sgsta':invoice_details.sgst_amount,
            'cgsta':invoice_details.cgst_amount,
            'ope_igst':invoice_details.ope_igst,
            'ope_sgst':invoice_details.ope_sgst,
            'ope_cgst':invoice_details.ope_cgst,
            'total_ope':invoice_details.total_ope,
            'invoice_paid_date':invoice_details.invoice_paid_date,
            'invoice_amount_paid':invoice_details.invoice_amount_paid,
            'is_invoice_paid':invoice_details.is_invoice_paid,  
        })
    return redirect("")
    
@login_required
def get_activities(request):
    if request.method == "POST":
        task_id = request.POST.get('task_id')
        task = Task.objects.get(id=task_id)
        activity = Task.objects.get(pk=task_id).activity.id
        return JsonResponse({'task':task.id,'activity' : activity})


@login_required
def partner_dashboard(request):
    ac = Client.objects.filter(assigned_partner_id = request.user.id)
    all_tasks = ClientTask.objects.filter(client__in = ac).count()
    pending_tasks = ClientTask.objects.filter(client__in = ac,is_approved_partner=False,is_completed=False,auditplan_id__isnull=False).count()
    completed_tasks = ClientTask.objects.filter(client__in = ac,is_approved_partner=True).count()
    rejected_tasks = ClientTask.objects.filter(client__in = ac,is_rejected=True).count()
    print(rejected_tasks)

    all_clients = Client.objects.filter(assigned_partner_id =request.user.id).count()
    billable_invoices = AuditPlanMapping.objects.filter(is_billable=True,client_id__in=ac).count()
    invoices_generated = AuditPlanMapping.objects.filter(invoice_number__isnull=False,client_id__in=ac).count()
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

    context_set={
        'all_tasks':all_tasks,
        'pending_tasks':pending_tasks,
        'completed_tasks':completed_tasks,
        'rejected_tasks' : rejected_tasks,
        'all_clients':all_clients,
        'billable_invoices':billable_invoices,
        'invoices_generated':invoices_generated,
        'invoices_notgenerated':invoices_notgenerated,
        'invoices_total':total
    }

    return render(request, 'partner/partner_dashboard.html', context_set)
