from django.conf.urls.defaults import *
from django_openstack.urls import get_topbar_name

topbar = get_topbar_name(__file__)
urlpatterns = patterns('',
    url(r'^new/$', 'django_openstack.fileupload.views.upload_file', name=topbar),
    url(r'^js/$', 'django_openstack.fileupload.views.upload_js'),
)

FEATURES = set(["fileupload"])
