from django.urls import path, re_path
from . import views

app_name = 'web'

urlpatterns = [
    path('', views.index,name='index'),
]
