from django.db import models

# Create your models here.
class MaxUsers(models.Model):
    main_client = models.CharField(max_length=20,null=True,blank=True)
    max_users = models.CharField(max_length=20,null=True,blank=True)
    current_users = models.CharField(max_length=20,null=True,blank=True)
    class Meta:
        db_table = 'maxusers'

class MaxFiles(models.Model):
    main_client = models.CharField(max_length=20,null=True,blank=True)
    max_files = models.CharField(max_length=20,null=True,blank=True)
    current_files = models.CharField(max_length=20,null=True,blank=True)
    class Meta:
        db_table = 'maxfiles'

class BillingDetails(models.Model):
    main_client = models.CharField(max_length=20,null=True,blank=True)
    account_type=models.CharField(max_length=20,default="Trial")
    bill_generation_date = models.DateTimeField(auto_now_add = True)
    start_date = models.DateField(auto_now=False)
    end_date = models.DateField(auto_now=False)
    current_date = models.DateField(auto_now=False)
    amount = models.CharField(max_length=100,default=0)
    transactionID = models.CharField(max_length=100)
    paymentmode = models.CharField(max_length=20,default="Online")
    payment_status = models.CharField(max_length=100,null=True,blank=True)
    created_by = models.CharField(max_length=20,null=True,blank=True)
    remarks = models.CharField(max_length=500,null=True,blank=True)
    modified_by = models.CharField(max_length=20,null=True,blank=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        db_table = 'billingdetails'

class BillingTransaction(models.Model):
    mainclient_identifier = models.CharField(max_length=100)
    key = models.CharField(max_length=100)
    txnid = models.CharField(max_length=100)
    productinfo = models.CharField(max_length=100)
    amount = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    surl = models.CharField(max_length=100)
    furl = models.CharField(max_length=100)
    hash = models.CharField(max_length=500)
    main_client = models.CharField(max_length=100)
    status = models.CharField(max_length=30)
    used = models.CharField(max_length=20,default="no",null=True,blank=True)
    archived = models.CharField(max_length=20,default="no",null=True,blank=True)
    class Meta:
        db_table = 'billingtransaction'

class TransactionDetails(models.Model):
    transactionID = models.CharField(max_length=50)
    mihpayid = models.CharField(max_length=50,null=True,blank=True)
    mode = models.CharField(max_length=50,null=True,blank=True)
    status = models.CharField(max_length=50,null=True,blank=True)
    unmappedstatus = models.CharField(max_length=50,null=True,blank=True)
    key = models.CharField(max_length=50,null=True,blank=True)
    amount = models.CharField(max_length=50,null=True,blank=True)
    cardCategory = models.CharField(max_length=50,null=True,blank=True)
    net_amount_debit = models.CharField(max_length=50,null=True,blank=True)
    addedon = models.CharField(max_length=50,null=True,blank=True)
    productinfo = models.CharField(max_length=50,null=True,blank=True)
    firstname =  models.CharField(max_length=50,null=True,blank=True)
    lastname = models.CharField(max_length=50,null=True,blank=True)
    email = models.CharField(max_length=50,null=True,blank=True)
    phone = models.CharField(max_length=50,null=True,blank=True)
    payment_source = models.CharField(max_length=50,null=True,blank=True)
    PG_TYPE = models.CharField(max_length=50,null=True,blank=True)
    bank_ref_num = models.CharField(max_length=50,null=True,blank=True)
    bankcode = models.CharField(max_length=50,null=True,blank=True)
    name_on_card = models.CharField(max_length=50,null=True,blank=True)
    cardnum = models.CharField(max_length=50,null=True,blank=True)
    class Meta:
        db_table = 'transactiondetails'

class TempTransaction(models.Model):
    main_client = models.CharField(max_length=100)
    transactionID = models.CharField(max_length=100)
    class Meta:
        db_table = 'temptransaction'

class UserFileCount(models.Model):
    user = models.CharField(max_length=100)
    count = models.CharField(max_length=100,default=0)
    class Meta:
        db_table = "userfilecount"
