from django.db import models
from datetime import datetime
from auditapp.models import User


class UserLink(models.Model):
    partner = models.CharField(max_length = 20,null=True,blank=True)
    employee = models.CharField(max_length = 20,null=True,blank=True)
    class Meta:
        db_table = "userlink"


# Level One
class Regulator(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    area_name = models.CharField(max_length=255,null=False,blank=False)
    type_of_audits =  models.CharField(max_length=20,null=False,blank=False)
    is_global = models.BooleanField(default=False)
    def __str__(self):
        return self.area_name

# Level Two
class Act(models.Model):
    act_name = models.CharField(max_length=255,null=False, blank=False)
    area = models.ForeignKey(Regulator, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return self.act_name
class Activity_Labels(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    activity_label_name = models.CharField(max_length=255, null=False,blank=False)
    is_global = models.BooleanField(default=False)
    def __str__(self):
        return self.activity_label_name
# Level Three
class Activity(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    activity_name = models.CharField(max_length=1024, null=False, blank=False)  
    activity_description = models.CharField(max_length=1024, null=False,blank=False, default="")
    label = models.ForeignKey(Activity_Labels,on_delete=models.CASCADE, blank=True, null=True)
    act = models.ForeignKey(Act, on_delete=models.CASCADE, blank=True, null=True, related_name='activity')
    process_notes = models.FileField(upload_to="activity_process_notes/", null=True, blank=True)
    is_global = models.BooleanField(default=False)
    def __str__(self):
        return self.activity_name

# Level Four
class Task(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    task_name = models.CharField(max_length=255, null=True, blank=True)
    task_estimated_days = models.CharField(max_length=255, null=True, blank=True)
    task_auditing_standard = models.CharField(max_length=255, null=True, blank=True)
    task_international_auditing_standard = models.CharField(max_length=255, null=True, blank=True)
    process_notes = models.FileField(upload_to="process_notes/", null=True, blank=True)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, blank=True, null=True, related_name='task')
    is_global = models.BooleanField(default=False)
    def __str__(self):
        return self.task_name

# Single Entity Tables
class AuditType(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    audit_type_name = models.CharField(max_length=255, null=False, blank=False)
    is_global = models.BooleanField(default=False)
    def __str__(self):
        return self.audit_type_name

class Entity(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    entity_name = models.CharField(max_length=255,null=False,blank=False)
    is_global = models.BooleanField(default=False)
    def __str__(self):
        return self.entity_name

class Industry(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    industry_name = models.CharField(max_length=255,null=False,blank=False)
    is_global = models.BooleanField(default=False)
    def __str__(self):
        return self.industry_name

class Audits(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    audit_name = models.CharField(max_length=255,null=False,blank=False)
    is_global = models.BooleanField(default=False)
    def __str__(self):
        return self.audit_names

# Client Based Tables
class Client(models.Model):
    client_name = models.CharField(max_length=255,null=False,blank=False)
    # client_start_date = models.DateField(auto_now_add=False,auto_now=False,blank=True, null=True) 
    # client_end_date = models.DateField(auto_now_add=False,auto_now=False,blank=True, null=True) 
    client_email = models.CharField(max_length=100 , null=False , blank=False , default="")
    finance_email = models.CharField(max_length=100 , null=False , blank=False , default="")
    pan_no = models.CharField(max_length=255, null=False, blank=False, default="")
    tan_no = models.CharField(max_length=255, null=False, blank=False, default="")
    gst_no = models.CharField(max_length=255, null=False, blank=False, default="")
    assigned_user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    assigned_partner = models.ForeignKey(User,related_name='partner', on_delete=models.SET_NULL, blank=True, null=True)
    user_id = models.CharField(max_length=255, null=True,blank=True)
    def __str__(self):
        return self.client_name
    
#auditplans
class AuditPlanMapping(models.Model):
    auditplanname = models.CharField(max_length=255,null=False,blank=False)
    start_date = models.DateField(auto_now_add=False,auto_now=False,blank=True, null=True) 
    estimated_end_date = models.DateField(auto_now_add=False,auto_now=False,blank=True, null=True)
    actual_end_date = models.DateField(auto_now_add=False,auto_now=False,blank=True, null=True)
    finance_year = models.CharField(max_length=20,null=True,blank=False)
    auditplan_frequency = models.CharField(max_length=20,null=True,blank=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=False, null=False)
    is_audit_plan_locked = models.BooleanField(default=False)
    is_billable = models.BooleanField(default=False)
    audittype = models.ForeignKey(AuditType, on_delete=models.CASCADE, blank=False, null=True)
    invoice_date = models.DateField(auto_now_add=True,auto_now=False,blank=True, null=True)
    invoice_number = models.CharField(max_length=255,null=True,blank=False)
    invoice_amount = models.CharField(max_length=255,null=True,blank=False,default=0)
    out_of_pocket_expenses = models.CharField(max_length=255,null=True,blank=False,default='0')
    ope_igst = models.FloatField(null=True,blank=False,default=0)
    ope_sgst = models.FloatField(null=True,blank=False,default=0)
    ope_cgst = models.FloatField(null=True,blank=False,default=0)
    total_ope = models.FloatField(null=True,blank=False,default=0)
    igst = models.FloatField(null=True,blank=False,default=0)
    cgst = models.FloatField(null=True,blank=False,default=0)
    sgst = models.FloatField(null=True,blank=False,default=0)
    igst_amount = models.FloatField(null=True,blank=False,default=0)
    cgst_amount = models.FloatField(null=True,blank=False,default=0)
    sgst_amount = models.FloatField(null=True,blank=False,default=0)
    is_invoice_paid = models.BooleanField(default=False,null=True)                                   
    invoice_paid_date = models.DateField(auto_now_add=True,auto_now=False,blank=True, null=True)
    invoice_amount_paid = models.FloatField(null=True,blank=False,default=0)
    def __str__(self):
        return self.auditplanname

class ClientTask(models.Model):
    act = models.ForeignKey(Act, on_delete=models.SET_NULL, blank=True, null=True)
    activity = models.ForeignKey(Activity, on_delete=models.SET_NULL, blank=True, null=True, related_name='client_task')
    auditplan = models.ForeignKey(AuditPlanMapping, on_delete=models.SET_NULL, blank=True, null=True)
    # audit_type = models.ForeignKey(AuditType, on_delete=models.SET_NULL, blank=True, null=True, related_name='client_audit_type')
    task_name = models.CharField(max_length=255, null=True, blank=True)
    task_estimated_days = models.CharField(max_length=255, null=True, blank=True)
    task_auditing_standard = models.CharField(max_length=255, null=True, blank=True)
    
    ##task samplings and relevance
    task_relevance = models.CharField(max_length=255, null=True, default=None)
    task_volume = models.CharField(max_length=255, null=True, default=None)
    task_sample_rate = models.CharField(max_length=255, null=True, default=None)

    task_type = models.CharField(max_length=255, null=True, blank=True)
    manager_feedback = models.CharField(max_length=255, null=True, blank=True)
    partner_feedback = models.CharField(max_length=255, null=True, blank=True)
    task_international_auditing_standard = models.CharField(max_length=255, null=True, blank=True)
    # task_master = models.ForeignKey(Task, on_delete=models.CASCADE, blank=True, null=True)
    # Dates fields are for Auditor and Article Holder
    task_start_date = models.DateField(auto_now_add=False,auto_now=False,blank=True, null=True) 
    task_end_date = models.DateField(auto_now_add=False,auto_now=False,blank=True, null=True) 
    task_start_datetime = models.DateTimeField(auto_now_add=False,auto_now=False,blank=True, null=True) 
    task_end_datetime = models.DateTimeField(auto_now_add=False,auto_now=False,blank=True, null=True) 
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    #status for approval
    status = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    is_approved_partner = models.BooleanField(default=False)
    # For attachment for which it will be sent for approval
    attachment_file = models.FileField(upload_to="task_submission/", null=True, blank=True)
    partner_attachment_file = models.TextField(null=True, blank=True)
    manager_attachment_file = models.TextField(null=True, blank=True)
    auditor_attachment_file = models.TextField(null=True, blank=True)
    article_attachment_file = models.TextField(null=True, blank=True)
    remark = models.CharField(max_length=255, null=True, blank=True)
    is_rejected=models.BooleanField(default=False)
    # Task Completed after Approval
    is_completed = models.BooleanField(default=False) 
    #start the project after assigned
    is_start = models.BooleanField(default=False)
    # reject task if don't want to work on it
    is_reject = models.BooleanField(default=False)
    #remark of rejection tasks
    rejection_remark = models.CharField(max_length=255, null=True, blank=True)
    #manager rejected task remark
    reject_task_remark = models.CharField(max_length=255, null=True, blank=True)
    notification = models.BooleanField(default=False)
    def __str__(self):
        return self.task_name


# Relationship Schemas
class ActivityAuditTypeEntity(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, blank=False, null=False)
    audittype = models.ForeignKey(AuditType, on_delete=models.CASCADE, blank=False, null=False)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, blank=False, null=False)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, blank=False, null=False)

class ClientIndustryAuditTypeEntity(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=False, null=False)
    audittype = models.ForeignKey(AuditType, on_delete=models.CASCADE, blank=False, null=False)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, blank=False, null=False)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, blank=False, null=False)

