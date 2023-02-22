from django.shortcuts import HttpResponseRedirect, HttpResponse


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
	return HttpResponseRedirect('/accounts/login')
	