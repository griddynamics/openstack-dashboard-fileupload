from django.http import HttpResponse
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.conf import settings
import os
from django import forms
from django.views.decorators.csrf import csrf_exempt
import re
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django import template


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
    return render_to_response('fileupload/picture_form.html', {'form': form,}, context_instance=template.RequestContext(request))

@login_required
@csrf_exempt
def upload_js(request):
    name = request.POST["name"]
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
        print ramdisk_num
        ramdisk_num = ramdisk_num.split()[-1]
        kernel_name = re.sub('[^\w.]', '_', request.FILES["kernel"].name)    
        p = os.popen("glance add name=%s disk_format=aki container_format=aki is_public=True < %s"%(name + "_" + kernel_name, path + kernel_name))
        kernel_num = p.read().split()[-1]
        image_name = re.sub('[^\w.]', '_', request.FILES["rootfs"].name)
        os.system("glance add name=%s disk_format=ami container_format=ami is_public=True ramdisk_id=%s kernel_id=%s < %s"%(name, ramdisk_num, kernel_num, path + image_name))
    else:
        kernel_num = p.read().split()[-1]
        image_name = re.sub('[^\w.]', '_', request.FILES["rootfs"].name)
        os.system("glance add name=%s disk_format=qcow2 container_format=qcow2 is_public=True < %s"%(name, path + image_name))
    return HttpResponse("success")