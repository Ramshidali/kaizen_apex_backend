from django.urls import path, re_path
from . import views

app_name = 'product'

urlpatterns = [
    path('category-list/', views.category_list, name='category_list'),
    re_path(r'^category-create/$', views.create_category, name='create_category'),
    re_path(r'^category-edit/(?P<pk>.*)/$', views.edit_category, name='edit_category'),
    re_path(r'^category-delete/(?P<pk>.*)/$', views.delete_category, name='delete_category'),
    
    path('product-list/', views.product_list, name='product_list'),
    re_path(r'^product-info/(?P<pk>.*)/$', views.product, name='product'),
    re_path(r'^create-product/$', views.create_product, name='create_product'),
    re_path(r'^edit-product/(?P<pk>.*)/$', views.edit_product, name='edit_product'),
    re_path(r'^product-delete/(?P<pk>.*)/$', views.delete_product, name='delete_product'),
    re_path(r'^edit-product-varient/(?P<pk>.*)/$', views.edit_varient, name='edit_varient'),
    re_path(r'^delete-product-varient/(?P<pk>.*)/$', views.delete_varient, name='delete_varient'),
]
