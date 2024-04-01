#standerd
import json
from datetime import date, datetime, timedelta
# django
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from product.models import Category
# local
from . models import *
from web.forms import AboutUsForm, BannerForm, BlogForm, ComplaintForm, ContactForm, CustomerReviewsForm, EnquiryForm, OurFeaturesForm
from main.decorators import role_required
from main.functions import generate_form_errors, get_auto_id

# Create your views here.
def index(request):
    today_date = timezone.now().date()
    last_month_start = (today_date - timedelta(days=today_date.day)).replace(day=1)
    about_us = {}
    banners = Banner.objects.filter(is_deleted=False).order_by("-date_added")
    if AboutUs.objects.filter(is_deleted=False).exists():
        about_us = AboutUs.objects.filter(is_deleted=False).latest('-date_added')
    our_features = OurFeatures.objects.filter(is_deleted=False)
    categories = Category.objects.filter(is_deleted=False)
    customer_reviews = CustomerReviews.objects.filter(is_deleted=False)
    blogs = Blog.objects.filter(is_deleted=False).order_by('-date_added')[:3]
    
    context = {
        "banners": banners,
        "about_us": about_us,
        "our_features": our_features,
        "categories": categories,
        "customer_reviews": customer_reviews,
        "blogs": blogs,
        "product_limit": 8,
        "varient_limit": 2,
        
        'page_title' : 'Home | KAIZEN APEX',
        'is_home': True,   
    }
  
    return render(request,'web/index.html', context)

def products(request):
    categories = Category.objects.filter(is_deleted=False)
    
    context = {
        "categories": categories,
        
        'page_title' : 'Products | KAIZEN APEX',
        'is_products': True,   
    }
  
    return render(request,'web/pages/products.html', context)

def about_us(request):
    
    context = {
        'page_title' : 'About Us | KAIZEN APEX',
        'is_about_us': True,   
    }
  
    return render(request,'web/pages/about.html', context)

def contact_us(request):
    instances = Contact.objects.filter(is_deleted=False)
    enquiry_form = EnquiryForm()
    
    main_branch = {}
    if instances.exists():
        main_branch = instances.filter(main=True).latest('-date_added')
    
    context = {
        'main_branch': main_branch,
        'enquiry_form': enquiry_form,
        'page_title' : 'Contact Us | KAIZEN APEX',
        'is_contact_us': True,   
    }
  
    return render(request,'web/pages/contact.html', context)

def add_enquiry(request):
    """
    create operation of enquiry
    :param request:
    :param pk:
    :return:
    """
    form = EnquiryForm(request.POST)
        
    if form.is_valid():
        data = form.save(commit=False)
        data.save()
        
        response_data = {
        "status": "true",
        "title": "Successfully Created",
        "message": "Enquiry created successfully.",
        'redirect': 'true',
        "redirect_url": reverse('web:contact_us')
        }
            
    else:
        message =generate_form_errors(form , formset=False)
        response_data = {
            "status": "false",
            "title": "Failed",
            "message": message,
        }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')

def add_complaint(request):
    """
    create operation of complaint
    :param request:
    :param pk:
    :return:
    """
    form = ComplaintForm(request.POST)
        
    if form.is_valid():
        data = form.save(commit=False)
        data.save()
        
        current_url = request.POST.get("current_url")
        
        response_data = {
        "status": "true",
        "title": "Successfully Created",
        "message": "Complaint created successfully.",
        'redirect': 'true',
        "redirect_url": current_url
        }
            
    else:
        message =generate_form_errors(form , formset=False)
        response_data = {
            "status": "false",
            "title": "Failed",
            "message": message,
        }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')

# ******************************************Admin Panel**********************************************#

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

    return render(request, 'admin_panel/pages/banner/list.html', context)

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
        form = BannerForm(request.POST,files=request.FILES)
            
        if form.is_valid():
            data = form.save(commit=False)
            data.auto_id = get_auto_id(Banner)
            data.creator = request.user
            data.date_updated = datetime.today()
            data.updater = request.user
            data.save()
            
            response_data = {
            "status": "true",
            "title": "Successfully Created",
            "message": "Banner created successfully.",
            'redirect': 'true',
            "redirect_url": reverse('web:banner_list')
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
            'url' : reverse('web:create_banner'),
            
            'is_purchase': True,
            'is_banner': True,
        }

        return render(request, 'admin_panel/pages/create/create.html',context)
    
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
                "redirect_url": reverse('web:banner_list')
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

        return render(request, 'admin_panel/pages/create/create.html',context)

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
        "redirect_url": reverse('web:banner_list'),
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')

@login_required
@role_required(['superadmin'])
def our_feature_list(request):
    """
    OurFeatures listings
    :param request:
    :return: OurFeatures list view
    """
    instances = OurFeatures.objects.filter(is_deleted=False).order_by("-date_added")
    
    context = {
        'instances': instances,
        'page_name' : 'Our Features',
        'page_title' : 'Our Features',
        
        'is_our_feature': True,
    }

    return render(request, 'admin_panel/pages/our_feature/list.html', context)

@login_required
@role_required(['superadmin'])
def create_our_feature(request):
    """
    create operation of OurFeatures
    :param request:
    :param pk:
    :return:
    """
    if request.method == 'POST':
        form = OurFeaturesForm(request.POST,files=request.FILES)
            
        if form.is_valid():
            data = form.save(commit=False)
            data.auto_id = get_auto_id(OurFeatures)
            data.creator = request.user
            data.date_updated = datetime.today()
            data.updater = request.user
            data.save()
            
            response_data = {
            "status": "true",
            "title": "Successfully Created",
            "message": "Our Features created successfully.",
            'redirect': 'true',
            "redirect_url": reverse('web:our_feature_list')
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
        
        form = OurFeaturesForm()

        context = {
            'form': form,
            'page_name' : 'Create Our Features',
            'page_title' : 'Create Our Features',
            'url' : reverse('web:create_our_feature'),
            
            'is_purchase': True,
            'is_our_feature': True,
        }

        return render(request, 'admin_panel/pages/create/create.html',context)
    
@login_required
@role_required(['superadmin'])
def edit_our_feature(request,pk):
    """
    edit operation of our_feature
    :param request:
    :param pk:
    :return:
    """
    instance = get_object_or_404(OurFeatures, pk=pk)
        
    message = ''
    if request.method == 'POST':
        form = OurFeaturesForm(request.POST,files=request.FILES,instance=instance)
        
        if form.is_valid():
            #update OurFeatures
            data = form.save(commit=False)
            data.date_updated = datetime.today()
            data.updater = request.user
            data.save()
                    
            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "OurFeatures Update successfully.",
                'redirect': 'true',
                "redirect_url": reverse('web:our_feature_list')
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
        
        form = OurFeaturesForm(instance=instance)

        context = {
            'form': form,
            'page_name' : 'Edit OurFeatures',
            'page_title' : 'Edit OurFeatures',
            
            'is_our_feature': True,
        }

        return render(request, 'admin_panel/pages/create/create.html',context)

@login_required
@role_required(['superadmin'])
def delete_our_feature(request, pk):
    """
    Our Features deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    instance = OurFeatures.objects.get(pk=pk)
    instance.is_deleted = True
    instance.save()
    
    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Our Features Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('web:our_feature_list'),
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
@role_required(['superadmin'])
def about_us_list(request):
    """
    AboutUs listings
    :param request:
    :return: AboutUs list view
    """
    instance = AboutUs.objects.filter(is_deleted=False).order_by("-date_added").first()
    
    context = {
        'instance': instance,
        'page_name' : 'Our Features',
        'page_title' : 'Our Features',
        
        'is_about_us': True,
    }

    return render(request, 'admin_panel/pages/about_us/list.html', context)

@login_required
@role_required(['superadmin'])
def create_about_us(request):
    """
    create operation of AboutUs
    :param request:
    :param pk:
    :return:
    """
    if request.method == 'POST':
        form = AboutUsForm(request.POST,files=request.FILES)
            
        if form.is_valid():
            data = form.save(commit=False)
            data.auto_id = get_auto_id(AboutUs)
            data.creator = request.user
            data.date_updated = datetime.today()
            data.updater = request.user
            data.save()
            
            response_data = {
            "status": "true",
            "title": "Successfully Created",
            "message": "Our Features created successfully.",
            'redirect': 'true',
            "redirect_url": reverse('web:about_us_list')
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
        
        form = AboutUsForm()

        context = {
            'form': form,
            'page_name' : 'Create Our Features',
            'page_title' : 'Create Our Features',
            'url' : reverse('web:create_about_us'),
            
            'is_purchase': True,
            'is_about_us': True,
        }

        return render(request, 'admin_panel/pages/create/create.html',context)
    
@login_required
@role_required(['superadmin'])
def edit_about_us(request,pk):
    """
    edit operation of about_us
    :param request:
    :param pk:
    :return:
    """
    instance = get_object_or_404(AboutUs, pk=pk)
        
    message = ''
    if request.method == 'POST':
        form = AboutUsForm(request.POST,files=request.FILES,instance=instance)
        
        if form.is_valid():
            #update AboutUs
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()
                    
            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "AboutUs Update successfully.",
                'redirect': 'true',
                "redirect_url": reverse('web:about_us_list')
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
        
        form = AboutUsForm(instance=instance)

        context = {
            'form': form,
            'page_name' : 'Edit AboutUs',
            'page_title' : 'Edit AboutUs',
            
            'is_purchase': True,
            'is_about_us': True,
        }

        return render(request, 'admin_panel/pages/create/create.html',context)

@login_required
@role_required(['superadmin'])
def delete_about_us(request, pk):
    """
    Our Features deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    instance = AboutUs.objects.get(pk=pk)
    instance.is_deleted = True
    instance.save()
    
    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Our Features Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('web:about_us_list'),
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')

@login_required
@role_required(['superadmin'])
def customer_review_info(request,pk):
    """
    Customer Reviews info
    :param request:
    :return: CustomerReviews info view
    """
    instances = CustomerReviews.objects.get(pk=pk,is_deleted=False)
    
    context = {
        'instances': instances,
        'page_name' : 'Customer Review',
        'page_title' : 'Customer Review',
        
        'is_customer_review': True,
    }

    return render(request, 'admin_panel/pages/customer_reviews/info.html', context)

@login_required
@role_required(['superadmin'])
def customer_review_list(request):
    """
    Customer Reviews listings
    :param request:
    :return: CustomerReviews list view
    """
    instances = CustomerReviews.objects.filter(is_deleted=False).order_by("-date_added")
    
    context = {
        'instances': instances,
        'page_name' : 'Customer Review',
        'page_title' : 'Customer Review',
        
        'is_customer_review': True,
    }

    return render(request, 'admin_panel/pages/customer_reviews/list.html', context)

def create_customer_review(request):
    """
    create operation of Customer Reviews
    :param request:
    :param pk:
    :return:
    """
    if request.method == 'POST':
        form = CustomerReviewsForm(request.POST,files=request.FILES)
            
        if form.is_valid():
            data = form.save(commit=False)
            data.save()
            
            response_data = {
            "status": "true",
            "title": "Successfully Created",
            "message": "Customer Review created successfully.",
            'redirect': 'true',
            "redirect_url": reverse('web:customer_review_list')
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
        
        form = CustomerReviewsForm()

        context = {
            'form': form,
            'page_name' : 'Create Customer Review',
            'page_title' : 'Create Customer Review',
            'url' : reverse('web:index'),
            
            'is_purchase': True,
            'is_customer_review': True,
        }

        return render(request, 'admin_panel/pages/create/create.html',context)
    
@login_required
def edit_customer_review(request,pk):
    """
    edit operation of customer_review
    :param request:
    :param pk:
    :return:
    """
    instance = get_object_or_404(CustomerReviews, pk=pk)
        
    message = ''
    if request.method == 'POST':
        form = CustomerReviewsForm(request.POST,files=request.FILES,instance=instance)
        
        if form.is_valid():
            #update CustomerReviews
            data = form.save(commit=False)
            data.save()
                    
            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Customer Reviews Update successfully.",
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
        
        form = CustomerReviewsForm(instance=instance)

        context = {
            'form': form,
            'page_name' : 'Edit Customer Reviews',
            'page_title' : 'Edit Customer Reviews',
            
            'is_purchase': True,
            'is_customer_review': True,
        }

        return render(request, 'admin_panel/pages/create/create.html',context)

@login_required
@role_required(['superadmin'])
def delete_customer_review(request, pk):
    """
    Customer Review deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    instance = CustomerReviews.objects.get(pk=pk)
    instance.is_deleted = True
    instance.save()
    
    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Customer Review Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('web:customer_review_list'),
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')

@login_required
@role_required(['superadmin'])
def info_blog(request,pk):
    """
    Blog info
    :param request:
    :return: Blog info view
    """
    instance = Blog.objects.get(pk=pk)
    
    context = {
        'instance': instance,
        'page_name' : 'Blog',
        'page_title' : 'Blog',
        
        'is_blog': True,
    }

    return render(request, 'admin_panel/pages/blog/info.html', context)

@login_required
@role_required(['superadmin'])
def blog_list(request):
    """
    Blog listings
    :param request:
    :return: Blog list view
    """
    instances = Blog.objects.filter(is_deleted=False).order_by("-date_added")
    
    context = {
        'instances': instances,
        'page_name' : 'Blog',
        'page_title' : 'Blog',
        
        'is_blog': True,
    }

    return render(request, 'admin_panel/pages/blog/list.html', context)

@login_required
@role_required(['superadmin'])
def create_blog(request):
    """
    create operation of Blog
    :param request:
    :param pk:
    :return:
    """
    if request.method == 'POST':
        form = BlogForm(request.POST,files=request.FILES)
            
        if form.is_valid():
            data = form.save(commit=False)
            data.auto_id = get_auto_id(Blog)
            data.creator = request.user
            data.date_added = datetime.today()
            data.save()
            
            response_data = {
            "status": "true",
            "title": "Successfully Created",
            "message": "Blog created successfully.",
            'redirect': 'true',
            "redirect_url": reverse('web:blog_list')
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
        
        form = BlogForm()

        context = {
            'form': form,
            'page_name' : 'Create Blog',
            'page_title' : 'Create Blog',
            'is_blog': True,
        }

        return render(request, 'admin_panel/pages/create/create.html',context)

@login_required
@role_required(['superadmin'])
def edit_blog(request,pk):
    """
    edit operation of blog
    :param request:
    :param pk:
    :return:
    """
    instance = get_object_or_404(Blog, pk=pk)
        
    message = ''
    if request.method == 'POST':
        form = BlogForm(request.POST,files=request.FILES,instance=instance)
        
        if form.is_valid():
            #update Blog
            data = form.save(commit=False)
            data.date_updated = datetime.today()
            data.updater = request.user
            data.save()
                    
            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Blog Update successfully.",
                'redirect': 'true',
                "redirect_url": reverse('web:blog_list')
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
        
        form = BlogForm(instance=instance)

        context = {
            'form': form,
            'page_name' : 'Edit Blog',
            'page_title' : 'Edit Blog',
            
            'is_blog': True,
        }

        return render(request, 'admin_panel/pages/create/create.html',context)

@login_required
@role_required(['superadmin'])
def delete_blog(request, pk):
    """
    Blog deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    instance = Blog.objects.get(pk=pk)
    instance.is_deleted = True
    instance.save()
    
    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Blog Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('web:blog_list'),
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')

@login_required
@role_required(['superadmin'])
def contact_list(request):
    """
    Contact listings
    :param request:
    :return: Contact list view
    """
    instances = Contact.objects.filter(is_deleted=False).order_by("-date_added")
    
    context = {
        'instances': instances,
        'page_name' : 'Contact',
        'page_title' : 'Contact',
        
        'is_contact': True,
    }

    return render(request, 'admin_panel/pages/contact/list.html', context)

@login_required
@role_required(['superadmin'])
def create_contact(request):
    """
    create operation of Contact
    :param request:
    :param pk:
    :return:
    """
    if request.method == 'POST':
        form = ContactForm(request.POST,files=request.FILES)
            
        if form.is_valid():
            data = form.save(commit=False)
            data.save()
            
            response_data = {
            "status": "true",
            "title": "Successfully Created",
            "message": "Contact created successfully.",
            'redirect': 'true',
            "redirect_url": reverse('web:contact_list')
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
        
        form = ContactForm()

        context = {
            'form': form,
            'page_name' : 'Create Contact',
            'page_title' : 'Create Contact',
            'url' : reverse('web:index'),
            
            'is_purchase': True,
            'is_contact': True,
        }

        return render(request, 'admin_panel/pages/create/create.html',context)

@login_required
@role_required(['superadmin'])
@login_required
def edit_contact(request,pk):
    """
    edit operation of contact
    :param request:
    :param pk:
    :return:
    """
    instance = get_object_or_404(Contact, pk=pk)
        
    message = ''
    if request.method == 'POST':
        form = ContactForm(request.POST,files=request.FILES,instance=instance)
        
        if form.is_valid():
            #update Contact
            data = form.save(commit=False)
            data.save()
                    
            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Contact Update successfully.",
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
        
        form = ContactForm(instance=instance)

        context = {
            'form': form,
            'page_name' : 'Edit Contact',
            'page_title' : 'Edit Contact',
            
            'is_purchase': True,
            'is_contact': True,
        }

        return render(request, 'admin_panel/pages/create/create.html',context)

@login_required
@role_required(['superadmin'])
def delete_contact(request, pk):
    """
    Contact deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    instance = Contact.objects.get(pk=pk)
    instance.is_deleted = True
    instance.save()
    
    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Contact Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('web:contact_list'),
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')

@login_required
@role_required(['superadmin'])
def complaint_info(request,pk):
    """
    Complaint info
    :param request:
    :return: Complaint info view
    """
    instance = Complaint.objects.get(pk=pk,is_deleted=False)
    
    context = {
        'instance': instance,
        'page_name' : 'Complaint',
        'page_title' : 'Complaint',
        
        'is_complaint': True,
    }

    return render(request, 'admin_panel/pages/complaints/info.html', context)

@login_required
@role_required(['superadmin'])
def complaint_list(request):
    """
    Complaint listings
    :param request:
    :return: Complaint list view
    """
    instances = Complaint.objects.filter(is_deleted=False).order_by("-date_added")
    
    context = {
        'instances': instances,
        'page_name' : 'Complaint',
        'page_title' : 'Complaint',
        
        'is_complaint': True,
    }

    return render(request, 'admin_panel/pages/complaints/list.html', context)

def create_complaint(request):
    """
    create operation of Complaint
    :param request:
    :param pk:
    :return:
    """
    if request.method == 'POST':
        form = ComplaintForm(request.POST,files=request.FILES)
            
        if form.is_valid():
            data = form.save(commit=False)
            data.save()
            
            response_data = {
            "status": "true",
            "title": "Successfully Created",
            "message": "Complaint created successfully.",
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
        
        form = ComplaintForm()

        context = {
            'form': form,
            'page_name' : 'Create Complaint',
            'page_title' : 'Create Complaint',
            'url' : reverse('web:index'),
            
            'is_purchase': True,
            'is_complaint': True,
        }

        return render(request, 'admin_panel/pages/create/create.html',context)

def edit_complaint(request,pk):
    """
    edit operation of complaint
    :param request:
    :param pk:
    :return:
    """
    instance = get_object_or_404(Complaint, pk=pk)
        
    message = ''
    if request.method == 'POST':
        form = ComplaintForm(request.POST,files=request.FILES,instance=instance)
        
        if form.is_valid():
            #update Complaint
            data = form.save(commit=False)
            data.save()
                    
            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Complaint Update successfully.",
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
        
        form = ComplaintForm(instance=instance)

        context = {
            'form': form,
            'page_name' : 'Edit Complaint',
            'page_title' : 'Edit Complaint',
            
            'is_purchase': True,
            'is_complaint': True,
        }

        return render(request, 'admin_panel/pages/create/create.html',context)

@login_required
@role_required(['superadmin'])
def delete_complaint(request, pk):
    """
    Complaint deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    instance = Complaint.objects.get(pk=pk)
    instance.is_deleted = True
    instance.save()
    
    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Complaint Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('web:complaint_list'),
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')

@login_required
@role_required(['superadmin'])
def enquiry_info(request,pk):
    """
    Enquiry info
    :param request:
    :return: Enquiry info view
    """
    instance = Enquiry.objects.get(pk=pk,is_deleted=False)
    
    context = {
        'instance': instance,
        'page_name' : 'Enquiry',
        'page_title' : 'Enquiry',
        
        'is_enquiry': True,
    }

    return render(request, 'admin_panel/pages/enquiry/info.html', context)

@login_required
@role_required(['superadmin'])
def enquiry_list(request):
    """
    Enquiry listings
    :param request:
    :return: Enquiry list view
    """
    instances = Enquiry.objects.filter(is_deleted=False).order_by("-date_added")
    
    context = {
        'instances': instances,
        'page_name' : 'Enquiry',
        'page_title' : 'Enquiry',
        
        'is_enquiry': True,
    }

    return render(request, 'admin_panel/pages/enquiry/list.html', context)

def create_enquiry(request):
    """
    create operation of Enquiry
    :param request:
    :param pk:
    :return:
    """
    if request.method == 'POST':
        form = EnquiryForm(request.POST,files=request.FILES)
            
        if form.is_valid():
            data = form.save(commit=False)
            data.save()
            
            response_data = {
            "status": "true",
            "title": "Successfully Created",
            "message": "Enquiry created successfully.",
            'redirect': 'true',
            "redirect_url": reverse('web:enquiry_list')
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
        
        form = EnquiryForm()

        context = {
            'form': form,
            'page_name' : 'Create Enquiry',
            'page_title' : 'Create Enquiry',
            
            'is_purchase': True,
            'is_enquiry': True,
        }

        return render(request, 'admin_panel/pages/create/create.html',context)

def edit_enquiry(request,pk):
    """
    edit operation of enquiry
    :param request:
    :param pk:
    :return:
    """
    instance = get_object_or_404(Enquiry, pk=pk)
        
    message = ''
    if request.method == 'POST':
        form = EnquiryForm(request.POST,files=request.FILES,instance=instance)
        
        if form.is_valid():
            #update Enquiry
            data = form.save(commit=False)
            data.save()
                    
            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Enquiry Update successfully.",
                'redirect': 'true',
                "redirect_url": reverse('web:enquiry_list')
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
        
        form = EnquiryForm(instance=instance)

        context = {
            'form': form,
            'page_name' : 'Edit Enquiry',
            'page_title' : 'Edit Enquiry',
            
            'is_purchase': True,
            'is_enquiry': True,
        }

        return render(request, 'admin_panel/pages/create/create.html',context)

@login_required
@role_required(['superadmin'])
def delete_enquiry(request, pk):
    """
    Enquiry deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    instance = Enquiry.objects.get(pk=pk)
    instance.is_deleted = True
    instance.save()
    
    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Enquiry Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('web:enquiry_list'),
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')