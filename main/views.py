#standerd
import json
import random
import datetime
#django
from django.urls import reverse
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User,Group
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect, HttpResponse
# third party
from main.forms import BranchesForm
from main.functions import generate_form_errors, get_auto_id
from main.models import Branches
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

@login_required
@role_required(['superadmin'])
def branch_list(request):
    """
    Branches listings
    :param request:
    :return: Branches list view
    """
    instances = Branches.objects.filter(is_deleted=False).order_by("-date_added")
    
    context = {
        'instances': instances,
        'page_name' : 'Branches',
        'page_title' : 'Branches',
        
        'is_branch': True,
    }

    return render(request, 'admin_panel/pages/branch/list.html', context)

@login_required
@role_required(['superadmin'])
def create_branch(request):
    """
    create operation of Branches
    :param request:
    :param pk:
    :return:
    """
    if request.method == 'POST':
        form = BranchesForm(request.POST,files=request.FILES)
            
        if form.is_valid():
            data = form.save(commit=False)
            data.auto_id = get_auto_id(Branches)
            data.creator = request.user
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()
            
            response_data = {
            "status": "true",
            "title": "Successfully Created",
            "message": "Branches created successfully.",
            'redirect': 'true',
            "redirect_url": reverse('web:index')
            }
                
        else:
            message =generate_form_errors(form , formset=False)
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:
        
        form = BranchesForm()

        context = {
            'form': form,
            'page_name' : 'Create Branches',
            'page_title' : 'Create Branches',
            'url' : reverse('web:index'),
            
            'is_purchase': True,
            'is_branch': True,
        }

        return render(request, 'admin_panel/pages/create/create.html',context)

@login_required
@role_required(['superadmin'])
def edit_branch(request,pk):
    """
    edit operation of branch
    :param request:
    :param pk:
    :return:
    """
    instance = get_object_or_404(Branches, pk=pk)
        
    message = ''
    if request.method == 'POST':
        form = BranchesForm(request.POST,files=request.FILES,instance=instance)
        
        if form.is_valid():
            #update Branches
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()
                    
            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Branches Update successfully.",
                'redirect': 'true',
                "redirect_url": reverse('web:idex')
            }
    
        else:
            message = generate_form_errors(form ,formset=False)
            
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    
    else:
        
        form = BranchesForm(instance=instance)

        context = {
            'form': form,
            'page_name' : 'Edit Branches',
            'page_title' : 'Edit Branches',
            
            'is_purchase': True,
            'is_branch': True,
        }

        return render(request, 'admin_panel/pages/create/create.html',context)

@login_required
@role_required(['superadmin'])
def delete_branch(request, pk):
    """
    Branches deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    instance = Branches.objects.get(pk=pk)
    instance.is_deleted = True
    instance.save()
    
    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Branches Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('web:branch_list'),
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')