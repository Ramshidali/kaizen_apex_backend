#standerd
import json
import datetime
#django
from django.db.models import Q,Min,Max
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponse
from django.db import transaction, IntegrityError
from django.contrib.auth.models import User,Group
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
#local
from . models import Category, Product, ProductVarient
from . forms import CategoryForm, ProductForm, ProductVarientForm
from main.decorators import role_required
from main.functions import encrypt_message, generate_form_errors, get_auto_id, has_group, paginate, randomnumber, send_email

# Create your views here.
@login_required
@role_required(['superadmin'])
def category_list(request):
    """
    Category listings
    :param request:
    :return: Category list view
    """
    instances = Category.objects.filter(is_deleted=False).order_by("-date_added")
    
    filter_data = {}
    query = request.GET.get("q")
    
    if query:

        instances = instances.filter(
            Q(name__icontains=query)
        )
        title = "Category - %s" % query
        filter_data['q'] = query
    
    context = {
        'instances': instances,
        'page_name' : 'Category',
        'page_title' : 'Category',
        'filter_data' :filter_data,
        
        'is_purchase': True,
        'is_category': True,
    }

    return render(request, 'admin_panel/pages/products/category_list.html', context)

@login_required
@role_required(['superadmin'])
def create_category(request):
    """
    create operation of Category
    :param request:
    :param pk:
    :return:
    """
    if request.method == 'POST':
        form = CategoryForm(request.POST)
            
        if form.is_valid():
            data = form.save(commit=False)
            data.auto_id = get_auto_id(Category)
            data.creator = request.user
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()
            
            response_data = {
            "status": "true",
            "title": "Successfully Created",
            "message": "Category created successfully.",
            'redirect': 'true',
            "redirect_url": reverse('product:category_list')
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
        
        form = CategoryForm()

        context = {
            'form': form,
            'page_name' : 'Create Category',
            'page_title' : 'Create Category',
            'url' : reverse('product:create_category'),
            
            'is_purchase': True,
            'is_category': True,
        }

        return render(request, 'admin_panel/pages/products/create_category.html',context)
    
@login_required
@role_required(['superadmin'])
def edit_category(request,pk):
    """
    edit operation of category
    :param request:
    :param pk:
    :return:
    """
    instance = get_object_or_404(Category, pk=pk)
        
    message = ''
    if request.method == 'POST':
        form = CategoryForm(request.POST,files=request.FILES,instance=instance)
        
        if form.is_valid():
            #update Category
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()
                    
            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Category Update successfully.",
                'redirect': 'true',
                "redirect_url": reverse('product:category_list')
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
        
        form = CategoryForm(instance=instance)

        context = {
            'form': form,
            'page_name' : 'Edit Category',
            'page_title' : 'Edit Category',
            
            'is_purchase': True,
            'is_category': True,
        }

        return render(request, 'admin_panel/pages/products/create_category.html',context)

@login_required
@role_required(['superadmin'])
def delete_category(request, pk):
    """
    Category deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    instance = Category.objects.get(pk=pk)
    instance.is_deleted = True
    instance.save()
    
    if Product.objects.filter(category=instance).exists():
        Product.objects.filter(category=instance).update(is_deleted=True)
        if ProductVarient.objects.filter(product__category=instance).exists():
            ProductVarient.objects.filter(product__category=instance).update(is_deleted=True)
    
    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Category Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('product:category_list'),
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')

login_required
@role_required(['superadmin'])
def product(request,pk):
    """
    Product Info
    :param request:
    :return: Product Info single view
    """
    
    instance = Product.objects.get(pk=pk,is_deleted=False)
    varients = ProductVarient.objects.filter(product=instance,is_deleted=False)

    context = {
        'instance': instance,
        'varients': varients,
        'page_name' : 'Product Info',
        'page_title' : 'Product Info',
    }

    return render(request, 'admin_panel/pages/products/product.html', context)

@login_required
@role_required(['superadmin'])
def product_list(request):
    """
    Products
    :param request:
    :return: Products list view
    """
    filter_data = {}
    
    instances = Product.objects.filter(is_deleted=False).order_by("-date_added")
    
    query = request.GET.get("q")
    if query:
        instances = instances.filter(
            Q(invoice_no__icontains=query) |
            Q(product_id__icontains=query) 
        )
        title = "Product Report - %s" % query
        filter_data['q'] = query
    
    context = {
        'instances': instances,
        'page_name' : 'Product Report',
        'page_title' : 'Product Report',
        'filter_data' :filter_data,
    }

    return render(request, 'admin_panel/pages/products/product_list.html', context)

@login_required
@role_required(['superadmin'])
def create_product(request):
    ProductVarientFormset = formset_factory(ProductVarientForm, extra=2)
    
    message = ''
    if request.method == 'POST':
        form_is_valid = False
        product_form = ProductForm(request.POST,request.FILES)
        product_varient_formset = ProductVarientFormset(request.POST,request.FILES,prefix='product_varient_formset', form_kwargs={'empty_permitted': False})
        
        if request.POST.get("have_varient") is None:
            if product_form.is_valid():
                form_is_valid = True
        else:
            if product_form.is_valid() and product_varient_formset.is_valid():
                form_is_valid = True
        
        if form_is_valid:
            try:
                with transaction.atomic():
                    product = product_form.save(commit=False)
                    product.auto_id = get_auto_id(Product)
                    product.creator = request.user
                    product.product = product
                    product.save()
                    
                    if product.have_varient :
                        for form in product_varient_formset:
                            data = form.save(commit=False)
                            data.auto_id = get_auto_id(ProductVarient)
                            data.creator = request.user
                            data.date_updated = datetime.datetime.today()
                            data.updater = request.user
                            data.product = product
                            data.save()
                    
                    response_data = {
                        "status": "true",
                        "title": "Successfully Created",
                        "message": "Product created successfully.",
                        'redirect': 'true',
                        "redirect_url": reverse('product:product_list')
                    }
                    
            except IntegrityError as e:
                # Handle database integrity error
                response_data = {
                    "status": "false",
                    "title": "Failed",
                    "message": str(e),
                }

            except Exception as e:
                # Handle other exceptions
                response_data = {
                    "status": "false",
                    "title": "Failed",
                    "message": str(e),
                }
        else:
            message = generate_form_errors(product_form, formset=False)
            
            if not request.POST.get("have_varient") is None:
                message += generate_form_errors(product_varient_formset, formset=True)
            
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    
    else:
        product_form = ProductForm()
        product_varient_formset = ProductVarientFormset(prefix='product_varient_formset')
        
        context = {
            'product_form': product_form,
            'product_varient_formset': product_varient_formset,
            
            'page_title': 'Create Product',
            'page_name' : 'create Product',
        }
        
        return render(request,'admin_panel/pages/products/create_product.html',context)
    
@login_required
@role_required(['superadmin'])
def edit_product(request,pk):
    """
    edit operation of product
    :param request:
    :param pk:
    :return:
    """
    product_instance = get_object_or_404(Product, pk=pk)
    varients = ProductVarient.objects.filter(product=product_instance)
    
    if ProductVarient.objects.filter(product=product_instance).exists():
        extra = 0
    else:
        extra = 1 

    ProductVarientFormset = inlineformset_factory(
        Product,
        ProductVarient,
        extra=extra,
        form=ProductVarientForm,
    )
        
    message = ''
    
    if request.method == 'POST':
        product_form = ProductForm(request.POST,request.FILES,instance=product_instance)
        product_varient_formset = ProductVarientFormset(request.POST,request.FILES,
                                        instance=product_instance,
                                        prefix='product_varient_formset',
                                        form_kwargs={'empty_permitted': False}) 
        
        if request.POST.get("have_varient") is None:
            if product_form.is_valid():
                form_is_valid = True
        else:
            if product_form.is_valid() and product_varient_formset.is_valid():
                form_is_valid = True
        
        if form_is_valid:   
                
            product = product_form.save(commit=False)
            product.date_updated = datetime.datetime.today()
            product.updater = request.user
            product.save()
            
            if product.have_varient :
                for form in product_varient_formset:
                    if form not in product_varient_formset.deleted_forms:
                        i_data = form.save(commit=False)
                        if not i_data.product :
                            i_data.product = product_instance
                        i_data.save()
                    
                for f in product_varient_formset.deleted_forms:
                    f.instance.delete()
            
            response_data = {
                "status": "true",
                "title": "Successfully Updated",
                "message": "Product Updated Successfully.",
                'redirect': 'true',
                "redirect_url": reverse('product:product_list'),
                "return" : True,
            }
    
        else:
            message = generate_form_errors(product_form,formset=False)
            
            if not request.POST.get("have_varient") is None:
                message += generate_form_errors(product_varient_formset,formset=True)
            
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
                        
    else:
        product_form = ProductForm(instance=product_instance)
        product_varient_formset = ProductVarientFormset(queryset=varients,
                                        prefix='product_varient_formset',
                                        instance=product_instance)
        
        context = {
            'product_form': product_form,
            'product_varient_formset': product_varient_formset,
            'page_name' : 'edit sale',
            'url' : reverse('product:edit_product', args=[product_instance.pk]),    
            
            'is_edit': True,        
        }

        return render(request, 'admin_panel/pages/products/create_product.html', context)
    
@login_required
@role_required(['superadmin'])
def delete_product(request, pk):
    """
    product deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    
    Product.objects.filter(pk=pk).update(is_deleted=True)
    if ProductVarient.objects.filter(product__pk=pk).exists():
        ProductVarient.objects.filter(product__pk=pk).update(is_deleted=True)
    
    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Product Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('product:product_list'),
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')

@login_required
@role_required(['superadmin'])
def edit_varient(request,pk):
    """
    edit operation of varient
    :param request:
    :param pk:
    :return:
    """
    instance = get_object_or_404(ProductVarient, pk=pk)
        
    message = ''
    if request.method == 'POST':
        form = ProductVarientForm(request.POST,files=request.FILES,instance=instance)
        
        if form.is_valid():
            #update Varient
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()
                    
            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Varient Update successfully.",
                'redirect': 'true',
                "redirect_url": reverse('product:product_list')
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
        
        form = ProductVarientForm(instance=instance)

        context = {
            'form': form,
            'page_name' : 'Edit Varient',
            'page_title' : 'Edit Varient',
        }

        return render(request, 'admin_panel/pages/create/create.html',context)

@login_required
@role_required(['superadmin'])
def delete_varient(request, pk):
    """
    Product Varient deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    instance = ProductVarient.objects.get(pk=pk)
    instance.is_deleted = True
    instance.save()
    
    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Varient Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('product:product_list'),
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')