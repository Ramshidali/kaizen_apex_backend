#standerd
from datetime import date, timedelta
#django
from django.utils import timezone
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from main.decorators import role_required
from main.functions import generate_form_errors
# third party
# local
from . models import *

# Create your views here.
def index(request):
    today_date = timezone.now().date()
    last_month_start = (today_date - timedelta(days=today_date.day)).replace(day=1)
    
    context = {
        'page_title' : 'Home | KAIZEN APEX',
        'is_dashboard': True,   
    }
  
    return render(request,'web/index.html', context)

@login_required
@role_required(['superadmin'])
def banner_list(request):
    """
    Banner listings
    :param request:
    :return: Banner list view
    """
    instances = Banner.objects.filter(is_deleted=False).order_by("-date_added")
    
    context = {
        'instances': instances,
        'page_name' : 'Banner',
        'page_title' : 'Banner',
        
        'is_banner': True,
    }

    return render(request, 'admin_panel/pages/products/banner_list.html', context)

@login_required
@role_required(['superadmin'])
def create_banner(request):
    """
    create operation of Banner
    :param request:
    :param pk:
    :return:
    """
    if request.method == 'POST':
        form = BannerForm(request.POST)
            
        if form.is_valid():
            data = form.save(commit=False)
            data.auto_id = get_auto_id(Banner)
            data.creator = request.user
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()
            
            response_data = {
            "status": "true",
            "title": "Successfully Created",
            "message": "Banner created successfully.",
            'redirect': 'true',
            "redirect_url": reverse('product:banner_list')
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
        
        form = BannerForm()

        context = {
            'form': form,
            'page_name' : 'Create Banner',
            'page_title' : 'Create Banner',
            'url' : reverse('product:create_banner'),
            
            'is_purchase': True,
            'is_banner': True,
        }

        return render(request, 'admin_panel/pages/products/create_banner.html',context)
    
@login_required
@role_required(['superadmin'])
def edit_banner(request,pk):
    """
    edit operation of banner
    :param request:
    :param pk:
    :return:
    """
    instance = get_object_or_404(Banner, pk=pk)
        
    message = ''
    if request.method == 'POST':
        form = BannerForm(request.POST,files=request.FILES,instance=instance)
        
        if form.is_valid():
            #update Banner
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()
                    
            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Banner Update successfully.",
                'redirect': 'true',
                "redirect_url": reverse('product:banner_list')
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
        
        form = BannerForm(instance=instance)

        context = {
            'form': form,
            'page_name' : 'Edit Banner',
            'page_title' : 'Edit Banner',
            
            'is_purchase': True,
            'is_banner': True,
        }

        return render(request, 'admin_panel/pages/products/create_banner.html',context)

@login_required
@role_required(['superadmin'])
def delete_banner(request, pk):
    """
    Banner deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    instance = Banner.objects.get(pk=pk)
    instance.is_deleted = True
    instance.save()
    
    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Banner Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('product:banner_list'),
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')