from django.urls import path, re_path
from . import views

app_name = 'product'

urlpatterns = [
    path('category-list/', views.category_list, name='category_list'),
    re_path(r'^category-create/$', views.create_category, name='create_category'),
    re_path(r'^category-edit/(?P<pk>.*)/$', views.edit_category, name='edit_category'),
    re_path(r'^category-delete/(?P<pk>.*)/$', views.delete_category, name='delete_category'),
]
