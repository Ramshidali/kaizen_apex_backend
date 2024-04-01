from django.urls import path, re_path
from . import views

app_name = 'web'

urlpatterns = [
    path('', views.index,name='index'),
    re_path(r'^products/$', views.products, name='products'),
    re_path(r'^about-us/$', views.about_us, name='about_us'),
    re_path(r'^contact-us/$', views.contact_us, name='contact_us'),
    re_path(r'^add-enquiry/$', views.add_enquiry, name='add_enquiry'),
    re_path(r'^add-complaint/$', views.add_complaint, name='add_complaint'),
    
    # Admin panel cruds
    
    path('banner-list/', views.banner_list, name='banner_list'),
    re_path(r'^banner-create/$', views.create_banner, name='create_banner'),
    re_path(r'^banner-edit/(?P<pk>.*)/$', views.edit_banner, name='edit_banner'),
    re_path(r'^banner-delete/(?P<pk>.*)/$', views.delete_banner, name='delete_banner'),
    
    path('our-features-list/', views.our_feature_list, name='our_feature_list'),
    re_path(r'^our-features-create/$', views.create_our_feature, name='create_our_feature'),
    re_path(r'^our-features-edit/(?P<pk>.*)/$', views.edit_our_feature, name='edit_our_feature'),
    re_path(r'^our-features-delete/(?P<pk>.*)/$', views.delete_our_feature, name='delete_our_feature'),
    
    path('about-us-list/', views.about_us_list, name='about_us_list'),
    re_path(r'^about-us-create/$', views.create_about_us, name='create_about_us'),
    re_path(r'^about-us-edit/(?P<pk>.*)/$', views.edit_about_us, name='edit_about_us'),
    re_path(r'^about-us-delete/(?P<pk>.*)/$', views.delete_about_us, name='delete_about_us'),
    
    path('cutomer-review-list/', views.customer_review_list, name='customer_review_list'),
    re_path(r'^cutomer-review-create/$', views.create_customer_review, name='create_customer_review'),
    re_path(r'^cutomer-review-info/(?P<pk>.*)/$', views.customer_review_info, name='info_customer_review'),
    re_path(r'^cutomer-review-edit/(?P<pk>.*)/$', views.edit_customer_review, name='edit_customer_review'),
    re_path(r'^cutomer-review-delete/(?P<pk>.*)/$', views.delete_customer_review, name='delete_customer_review'),
    
    path('blog-list/', views.blog_list, name='blog_list'),
    re_path(r'^blog-create/$', views.create_blog, name='create_blog'),
    re_path(r'^blog-info/(?P<pk>.*)/$', views.info_blog, name='info_blog'),
    re_path(r'^blog-edit/(?P<pk>.*)/$', views.edit_blog, name='edit_blog'),
    re_path(r'^blog-delete/(?P<pk>.*)/$', views.delete_blog, name='delete_blog'),
    
    path('contact-list/', views.contact_list, name='contact_list'),
    re_path(r'^contact-create/$', views.create_contact, name='create_contact'),
    re_path(r'^contact-edit/(?P<pk>.*)/$', views.edit_contact, name='edit_contact'),
    re_path(r'^contact-delete/(?P<pk>.*)/$', views.delete_contact, name='delete_contact'),
    
    path('complaint-list/', views.complaint_list, name='complaint_list'),
    re_path(r'^complaint-create/$', views.create_complaint, name='create_complaint'),
    re_path(r'^complaint-info/(?P<pk>.*)/$', views.complaint_info, name='info_complaint'),
    re_path(r'^complaint-edit/(?P<pk>.*)/$', views.edit_complaint, name='edit_complaint'),
    re_path(r'^complaint-delete/(?P<pk>.*)/$', views.delete_complaint, name='delete_complaint'),
    
    path('enquiry-list/', views.enquiry_list, name='enquiry_list'),
    re_path(r'^enquiry-create/$', views.create_enquiry, name='create_enquiry'),
    re_path(r'^enquiry-info/(?P<pk>.*)/$', views.enquiry_info, name='info_enquiry'),
    re_path(r'^enquiry-edit/(?P<pk>.*)/$', views.edit_enquiry, name='edit_enquiry'),
    re_path(r'^enquiry-delete/(?P<pk>.*)/$', views.delete_enquiry, name='delete_enquiry'),
]
