

login_required
@role_required(['superadmin'])
def product(request,pk):
    """
    Product Info
    :param request:
    :return: Product Info single view
    """
    
    instance = Product.objects.get(pk=pk)

    context = {
        'instance': instance,
        'page_name' : 'Product Info',
        'page_title' : 'Product Info',
    }

    return render(request, 'admin_panel/pages/product/product.html', context)

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
         
    date_range = request.GET.get('date_range')
    if date_range:
        start_date_str, end_date_str = date_range.split(' - ')
        start_date = datetime.datetime.strptime(start_date_str, '%m/%d/%Y').date()
        end_date = datetime.datetime.strptime(end_date_str, '%m/%d/%Y').date()
        instances = instances.filter(date__range=[start_date, end_date])
        filter_data['date_range'] = date_range
    
    query = request.GET.get("q")
    if query:
        instances = instances.filter(
            Q(invoice_no__icontains=query) |
            Q(product_id__icontains=query) 
        )
        title = "Product Report - %s" % query
        filter_data['q'] = query
    
        
    first_date_added = Product.objects.aggregate(first_date_added=Min('date'))['first_date_added']
    last_date_added = Product.objects.aggregate(last_date_added=Max('date'))['last_date_added']
    
    first_date_formatted = first_date_added.strftime('%m/%d/%Y') if first_date_added else None
    last_date_formatted = last_date_added.strftime('%m/%d/%Y') if last_date_added else None
        
    # print(branch)
    context = {
        'instances': instances,
        'first_date_formatted': first_date_formatted,
        'last_date_formatted': last_date_formatted,
        'page_name' : 'Product Report',
        'page_title' : 'Product Report',
        'filter_data' :filter_data,
    }

    return render(request, 'admin_panel/pages/product/product_list.html', context)

@login_required
@role_required(['superadmin'])
def add_product(request,branch_pk):
    ProductVarientFormset = formset_factory(ProductVarientForm, extra=2)
    
    message = ''
    if request.method == 'POST':
        product_form = ProductForm(request.FILES,request.POST)
        product_varient_formset = ProductVarientFormset(request.POST,prefix='product_varient_formset', form_kwargs={'empty_permitted': False})
        
        if product_form.is_valid() and product_varient_formset.is_valid():
            try:
                with transaction.atomic():
                    product = Product.objects.create(
                        #create product
                        auto_id = get_auto_id(Product),
                        creator = request.user,
                        date_updated = datetime.datetime.today(),
                        updater = request.user,
                    )
                    
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
            message += generate_form_errors(product_varient_formset, formset=True)
            
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    
    else:
        product_form = ProductForm(request.POST)
        product_varient_formset = ProductVarientFormset(prefix='product_varient_formset')
        
        context = {
            'product_form': product_form,
            'product_varient_formset': product_varient_formset,
            
            'page_title': 'Create Product',
            'page_name' : 'create Product',
        }
        
        return render(request,'admin_panel/pages/product/create_product.html',context)
    
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
                
        if product_varient_formset.is_valid():
            #create
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
            message = generate_form_errors(product_varient_formset,formset=True)
            
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
            'product_varient_formset': product_varient_formset,
            'message': message,
            'page_name' : 'edit sale',
            'url' : reverse('product:edit_product', args=[product_instance.pk]),            
        }

        return render(request, 'admin_panel/pages/product/create_product.html', context)