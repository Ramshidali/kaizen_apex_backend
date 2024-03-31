import datetime

from django import template
from django.db.models import Q, Sum
from django.contrib.auth.models import User, Group

from web.models import Contact

register = template.Library()

@register.simple_tag
def get_contacts():
    inatsnces = {}
    if (instances:=Contact.objects.filter(is_deleted=False)).exists():
        instances = instances.latest("-date_added")
    
    return instances