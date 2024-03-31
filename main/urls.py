from django.urls import path, re_path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index,name='index'),
    
    path('branch-list/', views.branch_list, name='branch_list'),
    re_path(r'^branch-create/$', views.create_branch, name='create_branch'),
    re_path(r'^branch-edit/(?P<pk>.*)/$', views.edit_branch, name='edit_branch'),
    re_path(r'^branch-delete/(?P<pk>.*)/$', views.delete_branch, name='delete_branch'),
]



