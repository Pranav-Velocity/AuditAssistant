from django.shortcuts import HttpResponseRedirect, HttpResponse , redirect , render
from django.contrib.auth import authenticate,get_user_model,login,logout
from auditapp.models import User
from partner.models import *
from main_client.models import *
from django.db.models import Q
from datetime import timedelta, date , datetime



def index(request):
	print("got this link")
	if(request.user.is_authenticated):
		if(request.user.is_main_client):
			return HttpResponseRedirect('/main_client')
		elif(request.user.is_super_admin):
			return HttpResponseRedirect('/superadmin')
		elif(request.user.is_partner):
			return HttpResponseRedirect('/partner')
		elif request.user.is_manager:
			return HttpResponseRedirect('/manager')
		elif request.user.is_auditorclerk:
			return HttpResponseRedirect('/auditor')
		elif request.user.is_articleholder:
			return HttpResponseRedirect('/article')
		elif request.user.is_developer_admin:
			return HttpResponseRedirect('/developers_console')
		else:
			return HttpResponseRedirect('/admin')
	return HttpResponseRedirect('/login')

def BillingCheck(user):
	get_billing_details = BillingDetails.objects.get(Q(main_client = user.id) & Q(is_active= True))
	end_date = str(get_billing_details.end_date)
	current_date = str(date.today())
	y1,m1,d1 = current_date.split('-')
	y2,m2,d2 = end_date.split('-')
	date_format = "%m/%d/%Y"
	a = datetime.strptime(f'{m1}/{d1}/{y1}', date_format)
	b = datetime.strptime(f'{m2}/{d2}/{y2}', date_format)
	delta = b - a
	remaining_days = delta.days
	# print("remaining_days :",remaining_days)
	return remaining_days

def LoginPage(request):
	error = ""
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		if username and password:
			authen = authenticate(username = username,password = password)
			if authen:
				# print(authen)
				if authen.is_super_admin:
					login(request,authen)
					return HttpResponseRedirect('/superadmin')
				elif authen.is_main_client:
					login(request,authen)
					return HttpResponseRedirect('/main_client')
				else:
					if authen.is_partner:
						main_client = User.objects.get(id = authen.linked_employee)
						remaining_days = BillingCheck(main_client)
						if remaining_days >= 0:
							login(request,authen)
							return HttpResponseRedirect('/partner')
						else:
							error = "Please Pay to Continue Services"
					elif authen.is_manager:
						partner = User.objects.get(id = authen.linked_employee)
						main_client = User.objects.get(id = partner.linked_employee)
						remaining_days = BillingCheck(main_client)
						if remaining_days >= 0:
							login(request,authen)
							return HttpResponseRedirect('/manager')
						else:
							error = "Please Pay to Continue Services"
					elif authen.is_auditorclerk:
						manager = User.objects.get(id = authen.linked_employee)
						partner = User.objects.get(id = manager.linked_employee)
						main_client = User.objects.get(id = partner.linked_employee)
						remaining_days = BillingCheck(main_client)
						if remaining_days >= 0:
							login(request,authen)
							return HttpResponseRedirect('/auditor')
						else:
							error = "Please Pay to Continue Services"
					elif authen.is_articleholder:
						manager = User.objects.get(id = authen.linked_employee)
						partner = User.objects.get(id = manager.linked_employee)
						main_client = User.objects.get(id = partner.linked_employee)
						remaining_days = BillingCheck(main_client)
						if remaining_days >= 0:
							login(request,authen)
							return HttpResponseRedirect('/article')
						else:
							error = "Please Pay to Continue Services"
				# login(request,authen)

				# if(request.user.is_authenticated):
				# 	if(request.user.is_main_client):
				# 		return HttpResponseRedirect('/main_client')
				# 	elif(request.user.is_super_admin):
				# 		return HttpResponseRedirect('/superadmin')
				# 	elif(request.user.is_partner):
				# 		return HttpResponseRedirect('/partner')
				# 	elif request.user.is_manager:
				# 		return HttpResponseRedirect('/manager')
				# 	elif request.user.is_auditorclerk:
				# 		return HttpResponseRedirect('/auditor')
				# 	elif request.user.is_articleholder:
				# 		return HttpResponseRedirect('/article')
				# 	elif request.user.is_developer_admin:
				# 		return HttpResponseRedirect('/developers_console')
				# 	else:
				# 		return HttpResponseRedirect('/admin')
				# return HttpResponseRedirect('/login')
	params = {
		"error":error
	}
	return render(request,"includes/login.html",params)

def Logout_page(request):
    logout(request)
    return redirect('login')