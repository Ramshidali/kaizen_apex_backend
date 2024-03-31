from django.contrib import admin
from django.views.static import serve
from django.urls import  include, path, re_path
from . import settings
from main import views as general_views
from ckeditor_uploader import views as ckeditor_views

urlpatterns = [
    path('ckeditor/', include('ckeditor_uploader.urls')), 
    path('',include(('web.urls'),namespace='web')),
    
    path('admin/', admin.site.urls),
    path('app/accounts/', include('registration.backends.default.urls')),
    path('kaizen-super-admin/',general_views.app,name='app'),
    path('kaizen-super-admin/main/',include(('main.urls'),namespace='main')), 
    
    # admin panel
    path('kaizen-admin/product/',include(('product.urls'),namespace='product')),
    
    # web
    
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT})
]
