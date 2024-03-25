#standerd
import json
import random
import datetime
#django
from django.urls import reverse
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User,Group
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect, HttpResponse
# third party
from rest_framework import status
#local
from main.decorators import role_required

# Create your views here.
@login_required
def app(request):
  
    return HttpResponseRedirect(reverse('main:index'))

# Create your views here.
@login_required
@role_required(['superadmin'])
def index(request):
    
    context = {
        'page_name' : 'Dashboard',
    }
  
    return render(request,'admin_panel/index.html', context)