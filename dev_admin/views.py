from django.shortcuts import render
from subprocess import run,PIPE
from .createdb import createnewdatabase
import sys
import os
# Create your views here.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
def index(request):
    return render(request, 'developers/devindex.html', {})

def createnewcafirm(request):
    if request.method == "POST":
        dbname = request.POST.get('firm_name')

        createnewdatabase(dbname)
    return render(request,'developers/devindex.html',{})

def casetup(request):
    return render(request,'developers/casetup.html',{})