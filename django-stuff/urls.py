from django.conf.urls.defaults import *
from django.contrib import admin

from controle.views import *
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^pylan/', include('pylan.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root':'/srv/pylan/media'}),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)',admin.site.root),
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^computadores/(.*)',computadores),  
    ('^hello/$',hello),
    ('^ajax/$',ajax),
    ('^$',index),
    ('^json/$',json),
)
