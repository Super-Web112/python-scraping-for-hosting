# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django import template
from app.models import ItalianName, City
import csv
import os
from zipfile import ZipFile
import io
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from app.models import User


from django.contrib.auth import authenticate
from django.forms.utils import ErrorList
from authentication.forms import SignUpForm

@login_required(login_url="/login/")
def index(request):
    
    context = {}
    context['segment'] = 'index'
    context['page_name'] = 'Scrape'
    context['cities'] = City.objects.all()

    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def user_management(request):
    
    msg     = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg     = 'User created'
            success = True
            
            #return redirect("/login/")

        else:
            msg = 'Form is not valid'    
    else:
        form = SignUpForm()



    context = {}
    context['segment'] = 'user-management.html'
    context['page_name'] = 'User Management'
    context['users'] = User.objects.all()
    context['form'] = form
    context['msg'] = msg
    context['success'] = success

    html_template = loader.get_template( 'user-management.html' )
    return HttpResponse(html_template.render(context, request))

def user_profile(request):
    
    context = {}
    context['segment'] = 'page-user.html'
    context['page_name'] = 'User Profile'

    html_template = loader.get_template( 'page-user.html' )
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def down(request):
    filename = request.path.split('/')[-1]
    s = io.BytesIO()
    zf = ZipFile(s, "w")
    zf.write('csv_files/'+filename)
    zf.close()
    response = HttpResponse(s.getvalue(), content_type='application/zip')
    response_filename = filename.replace('csv', 'zip')
    response['Content-Disposition'] = 'attachment; filename=%s' % response_filename
    # response['Content-Length'] = zip_io.tell()
    return response

@login_required(login_url="/login/")
def upload_photo(request):
    if request.method == 'POST' and request.is_ajax():
        image = request.FILES['image']
        username = request.POST.get('username', None)
        image_types = [
            'image/png', 'image/jpg',
            'image/jpeg', 'image/pjpeg', 'image/gif'
        ]
        if image.content_type not in image_types:
            data = json.dumps({
                'status': 405,
                'error': _('Bad image format.')
            })
            return HttpResponse(
                data, content_type="application/json", status=405)
        if os.path.exists(settings.UPLOAD_PATH + username + '.' + image.content_type.split("/")[-1]):
            os.remove(settings.UPLOAD_PATH + username + '.' + image.content_type.split("/")[-1])
        tmp_file = os.path.join(settings.UPLOAD_PATH, username + '.' + image.content_type.split("/")[-1])
        path = default_storage.save(tmp_file, ContentFile(image.read()))
        img_url = os.path.join(settings.MEDIA_URL, path)
        user_photo = User.objects.get(username=username)
        user_photo.photo = 'static/assets/img/upload/' + username + '.' + image.content_type.split("/")[-1]
        user_photo.save()
        data = {
            'status': 200,
            'name': username + '.' + image.content_type.split("/")[-1]
        }
        return JsonResponse(data, content_type='application/json')
    return HttpResponse(_('Invalid request!'))

@login_required(login_url="/login/")
def update_profile(request):
    if request.method == 'POST':
        userId = request.POST.get('userId', None)
        print(userId)
        userName = request.POST.get('userName', None)
        email = request.POST.get('email', None)
        firstname = request.POST.get('firstname', None)
        lastname = request.POST.get('lastname', None)
        address = request.POST.get('address', None)
        city = request.POST.get('city', None)
        country = request.POST.get('country', None)
        postalCode = request.POST.get('postalCode', None)
        aboutMe = request.POST.get('aboutMe', None)

        user = User.objects.get(username=userName)
        user.username = userName
        user.email = email
        user.first_name = firstname
        user.last_name = lastname
        user.address = address
        user.city = city
        user.country = country
        user.postal_code = postalCode
        user.aboutMe = aboutMe
        user.save()
    return HttpResponseRedirect('/user-profile')

@login_required(login_url="/login/")
def del_user(request):
    if request.method == 'POST':
        userName = request.POST.get('username', None)
        print(userName)
        user = User.objects.get(username=userName)
        user.delete()
    
    HttpResponse('Deleted successfully!')


# @login_required(login_url="/login/")
# def pages(request):

#     context = {}
#     # All resource paths end in .html.
#     # Pick out the html file name from the url. And load that template.
#     try:
        
#         load_template      = request.path.split('/')[-1]
#         context['segment'] = load_template

#         html_template = loader.get_template( load_template )
#         return HttpResponse(html_template.render(context, request))
        
#     except template.TemplateDoesNotExist:

#         html_template = loader.get_template( 'page-404.html' )
#         return HttpResponse(html_template.render(context, request))

#     except:
    
#         html_template = loader.get_template( 'page-500.html' )
#         return HttpResponse(html_template.render(context, request))
