import datetime

from django import template
from django.db.models import Q, Sum
from django.contrib.auth.models import User, Group

from web.forms import ComplaintForm
from web.models import AboutUs, CustomerReviews,OurFeatures

register = template.Library()

@register.simple_tag
def get_customer_reviews():
    instances = {}
    if (instances:=CustomerReviews.objects.filter(is_deleted=False)).exists():
        instances = instances.order_by("-date_added")
    return instances

@register.simple_tag
def get_our_features():
    instances = {}
    if (instances:=OurFeatures.objects.filter(is_deleted=False)).exists():
        instances = instances.order_by("-date_added")
    return instances

@register.simple_tag
def get_about_us():
    instances = {}
    if (instances:=AboutUs.objects.filter(is_deleted=False)).exists():
        instances = instances.latest('-date_added')
    return instances

@register.simple_tag
def complaint_form():
    return ComplaintForm()
