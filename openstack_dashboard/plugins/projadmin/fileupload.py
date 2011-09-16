import os
import re
import shutil

from django.http import HttpResponse
from django.utils import simplejson
from django.conf import settings
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django import template
from django.conf.urls.defaults import *
from django.contrib import messages
from django.core.urlresolvers import reverse

from openstack_dashboard.plugins import get_topbar_name


topbar = get_topbar_name(__file__)
urlpatterns = patterns(__name__,
    url(r'^fileupload/new/$', 'upload_file', name=topbar + "/fileupload"),
    url(r'^fileupload/js/$', 'upload_js', name=topbar + "/upload_js"),
    url(r'^fileupload/forward/$', 'forward', name=topbar + "/forward"),
)

FEATURES = set(["fileupload"])


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    kernel = forms.FileField()
    initrd = forms.FileField()
    rootfs = forms.FileField()


def handle_uploaded_file(f, path):
    file_name = re.sub('[^\w.]', '_', f.name)
    destination = open(path + file_name, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()


@login_required
@csrf_exempt
def upload_file(request):
    form = UploadFileForm()
    return render_to_response('fileupload/upload_form.html', {'form': form,}, context_instance=template.RequestContext(request))


@login_required
@csrf_exempt
def upload_js(request):
    name = re.sub('[^\w.]', '_', request.POST["name"])
    path = '/tmp/' + request.COOKIES["sessionid"] + "/"

    try:
        os.mkdir(path)
    except:
        pass
    for key in request.FILES.keys():
        handle_uploaded_file(request.FILES[key], path)

    if len(request.FILES.keys()) == 3:
        ramdisk_name = re.sub('[^\w.]', '_', request.FILES["initrd"].name)
        p = os.popen("glance add name=%s disk_format=ari container_format=ari is_public=True < %s"%(name + "_" + ramdisk_name, path + ramdisk_name))
        ramdisk_num = p.read()
        ramdisk_num = ramdisk_num.split()[-1]
        kernel_name = re.sub('[^\w.]', '_', request.FILES["kernel"].name)    
        p = os.popen("glance add name=%s disk_format=aki container_format=aki is_public=True < %s"%(name + "_" + kernel_name, path + kernel_name))
        kernel_num = p.read().split()[-1]
        image_name = re.sub('[^\w.]', '_', request.FILES["rootfs"].name)
        p = os.popen("glance add name=%s disk_format=ami container_format=ami is_public=True ramdisk_id=%s kernel_id=%s < %s"%(name, ramdisk_num, kernel_num, path + image_name))
    else:
        image_name = re.sub('[^\w.]', '_', request.FILES["rootfs"].name)
        p = os.popen("glance add name=%s disk_format=qcow2 container_format=ovf is_public=True < %s"%(name, path + image_name))
    id = p.read().split()[-1]
    shutil.rmtree(path)
    
    request.session['image_name'] = name
    request.session['image_id'] = id
    
    return HttpResponse("success")

@login_required
def forward(request):
    messages.info(request, "Image %s appended with id %s" % (request.session['image_name'], request.session['image_id']))
    return redirect(reverse("projadmin/images"))
