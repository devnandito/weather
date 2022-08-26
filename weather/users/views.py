# coding=utf-8

# Django
from django.shortcuts import reverse, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth import update_session_auth_hash
from django.core.paginator import Paginator, InvalidPage, EmptyPage

# Models
from weather.users.models import User, Profile
from weather.levels.models import Level

# Forms
from weather.users.forms import CustomUserCreationForm, CustomUserChangeForm, ProfileForm, ProfileUserForm, CustomMetCreationForm

# Utilities
from weather.utils.functions import get_url, get_body, get_button

# Python
from config.settings import base
import smtplib
import os, folium

def get_name():
    name = ['Usuarios', 'usuarios', 'Usuario', 'usuario', 'Perfiles', 'perfiles', 'Perfil', 'perfil', 'Tablero', 'password', 'Arasunu Weather']
    return name

@login_required()
def dashboard(request):
    template = loader.get_template('users/dashboard.html')
    shp_dir = os.path.join(os.getcwd(),'media','shp')

    tmp = get_name()

    # folium
    m = folium.Map(location=[-25.3080,-57.5629],zoom_start=8)

    ## style
    style_basin = {'fillColor': '#228B22', 'color': '#228B22'}
    style_rivers = { 'color': 'blue'}
    style_cities = { 'color': 'red'}

    ## adding to view
    # folium.GeoJson(os.path.join(shp_dir,'basin.geojson'),name='basin',style_function=lambda x:style_basin).add_to(m)
    # folium.GeoJson(os.path.join(shp_dir,'estaciones.geojson'),name='estaciones',style_function=lambda x:style_rivers).add_to(m)
    # folium.GeoJson(os.path.join(shp_dir,'Hidrografia_Asuncion.geojson'),style_function=lambda x:style_rivers).add_to(m)
    folium.GeoJson(os.path.join(shp_dir,'Barrios_Localidades_Asuncion.geojson'),style_function=lambda x:style_rivers).add_to(m)
    # folium.GeoJson(os.path.join(shp_dir,'output.json'),style_function=lambda x:style_rivers).add_to(m)
    folium.LayerControl().add_to(m)
    
    m=m._repr_html_()
    context = {
        'title': get_body(tmp[10], tmp[10]),
        'my_map': m,
    }
    return HttpResponse(template.render(context, request))

@login_required()
def show_user(request):
    tmp = get_name()
    list_title = ['#', 'Usuario', 'Email', 'Nombre', 'Apellido', 'Foto', 'Perfil', 'Estado', 'Ultimo login', 'Acciones']
    template = loader.get_template('users/show.html')
    list_paginator = User.objects.all()
    paginator = Paginator(list_paginator, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        object_list = paginator.page(page)
    except (EmptyPage, InvalidPage):
        object_list = paginator.page(paginator.num_pages)
    context = {
        'title': get_body(tmp[3], tmp[0]),
        'object_list': object_list,
        'uri': get_url('users'),
        'list_title':list_title,
    }
    return HttpResponse(template.render(context, request))

@login_required()
def create_user(request):
    tmp = get_name()
    button = get_button()
    template = loader.get_template('users/add.html')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        form1 = ProfileUserForm(request.POST, request.FILES)
        if form.is_valid() and form1.is_valid():
            user = form.save()
            profile = form1.save(commit=False)
            profile.user = user
            profile.save()
            message = 'Los datos se guardaron correctamente!'
            tpl = loader.get_template('messages/message.html')
            contextSuccess = {
                'title': get_body(tmp[3], tmp[0]),
                'uri': get_url('users'),
                'message': message,
            }
            return HttpResponse(tpl.render(contextSuccess, request))
    else:
        form = CustomUserCreationForm()
        form1 = ProfileUserForm()
    context = {
        'title': get_body(tmp[3], tmp[0]),
        'form': form,
        'form1': form1,
        'uri': get_url('users'),
        'button': button[1],
    }
    return HttpResponse(template.render(context, request))

@login_required()
def edit_user(request, pk):
    tmp = get_name()
    button = get_button()
    template = loader.get_template('users/edit.html')
    ins = get_object_or_404(User, pk=pk)
    ins1 = get_object_or_404(Profile, user=pk)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=ins)
        form1 = ProfileUserForm(request.POST, request.FILES,  instance=ins1)
        if form.is_valid() and form1.is_valid():
            form.save()
            form1.save()
            message = 'Los datos se guardaron correctamente!'
            tpl = loader.get_template('messages/message.html')
            contextSuccess = {
                'title': get_body(tmp[3], tmp[0]),
                'uri': get_url('users'),
                'message': message,
            }
            return HttpResponse(tpl.render(contextSuccess, request))
    else:
        form = CustomUserChangeForm(instance=ins)
        form1 = ProfileUserForm(instance=ins1)
    context = {
        'title': get_body(tmp[3], tmp[0]),
        'form': form,
        'form1': form1,
        'uri': get_url('users'),
        'button': button[1],
    }
    return HttpResponse(template.render(context, request))

@login_required()
def delete_user(request, pk):
    tmp = get_name()
    button = get_button()
    template = loader.get_template('users/delete.html')
    object_list = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        object_list.delete()
        return HttpResponseRedirect(reverse('users:show'))
    else:
        context = {
            'title': get_body(tmp[3], tmp[0]),
            'object_list': object_list,
            'uri': get_url('users'),
            'button': button[3],
        }
    return HttpResponse(template.render(context, request))

@login_required()
def set_pwd(request, pk):
    tmp = get_name()
    template = loader.get_template('users/changepwd.html')
    ins = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = SetPasswordForm(ins, request.POST)
        if form.is_valid():
            form.save()
            message = 'Los datos se guardaron correctamente!'
            tpl = loader.get_template('messages/message.html')
            contextSuccess = {
                'title': get_body(tmp[3], tmp[0]),
                'uri': get_url('users'),
                'message': message,
            }
            return HttpResponse(tpl.render(contextSuccess, request))
    else:
        form = SetPasswordForm(ins)
    context = {
        'title': get_body(tmp[9], tmp[9]),
        'form': form,
        'uri': get_url('users'),
    }
    return HttpResponse(template.render(context, request))

@login_required()
def change_pwd(request, pk):
    tmp = get_name()
    template = loader.get_template('users/changepwd.html')
    ins = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = PasswordChangeForm(ins, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            message = 'Los datos se guardaron correctamente!'
            tpl = loader.get_template('messages/message.html')
            contextSuccess = {
                'title': get_body(tmp[3], tmp[0]),
                'uri': get_url('users'),
                'message': message,
            }
            return HttpResponse(tpl.render(contextSuccess, request))
    else:
        form = PasswordChangeForm(ins)
    context = {
        'title': get_body(tmp[9], tmp[9]),
        'form': form,
        'uri': get_url('users'),
    }
    return HttpResponse(template.render(context, request))

@login_required()
def show_profile(request):
    tmp = get_name()
    list_title = ['#', 'Usuario', 'Descripción', 'Perfil', 'Foto', 'Acciones']
    template = loader.get_template('profiles/show.html')
    list_paginator = Profile.objects.all()
    paginator = Paginator(list_paginator, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        object_list = paginator.page(page)
    except (EmptyPage, InvalidPage):
        object_list = paginator.page(paginator.num_pages)
    context = {
        'title': get_body(tmp[7], tmp[4]),
        'object_list': object_list,
        'uri': get_url('users'),
        'list_title':list_title,
    }
    return HttpResponse(template.render(context, request))

@login_required()
def create_profile(request):
    tmp = get_name()
    button = get_button()
    template = loader.get_template('profiles/add.html')
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            message = 'Los datos se guardaron correctamente!'
            tpl = loader.get_template('messages/message.html')
            contextSuccess = {
                'title': get_body(tmp[7], tmp[4]),
                'uri': get_url('users'),
                'message': message,
            }
            return HttpResponse(tpl.render(contextSuccess, request))
    else:
        form = ProfileForm()
    context = {
        'title': get_body(tmp[7], tmp[4]),
        'form': form,
        'uri': get_url('users'),
        'button': button[1],
    }
    return HttpResponse(template.render(context, request))

@login_required()
def edit_profile(request, pk):
    tmp = get_name()
    button = get_button()
    template = loader.get_template('profiles/edit.html')
    ins = get_object_or_404(Profile, pk=pk)
    if request.method == 'POST':
        form = ProfileUserForm(request.POST, request.FILES, instance=ins)
        if form.is_valid():
            form.save()
            message = 'Los datos se guardaron correctamente!'
            tpl = loader.get_template('messages/message.html')
            contextSuccess = {
                'title': get_body(tmp[7], tmp[4]),
                'uri': get_url('users'),
                'message': message,
            }
            return HttpResponse(tpl.render(contextSuccess, request))
    else:
        form = ProfileUserForm(instance=ins)
    context = {
        'title': get_body(tmp[7], tmp[4]),
        'form': form,
        'uri': get_url('users'),
        'button': button[1],
    }
    return HttpResponse(template.render(context, request))

@login_required()
def delete_profile(request, pk):
    tmp = get_name()
    button = get_button()
    template = loader.get_template('profiles/delete.html')
    object_list = get_object_or_404(Profile, user=pk)
    if request.method == 'POST':
        object_list.delete()
        return HttpResponseRedirect(reverse('users:showprofile'))
    else:
        context = {
            'title': get_body(tmp[7], tmp[4]),
            'object_list': object_list,
            'uri': get_url('users'),
            'button': button[3],
        }
    return HttpResponse(template.render(context, request))

@login_required()
def show_met(request):
    tmp = get_name()
    list_title = ['#', 'Usuario', 'Email', 'Nombre', 'Apellido', 'Foto', 'Perfil', 'Estado', 'Ultimo login', 'Acciones']
    template = loader.get_template('users/list_met.html')
    list_paginator = User.objects.filter(profile__level__id=2)
    paginator = Paginator(list_paginator, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        object_list = paginator.page(page)
    except (EmptyPage, InvalidPage):
        object_list = paginator.page(paginator.num_pages)
    context = {
        'title': get_body(tmp[3], tmp[0]),
        'object_list': object_list,
        'uri': get_url('users'),
        'list_title':list_title,
    }
    return HttpResponse(template.render(context, request))

@login_required()
def create_met(request):
    my_email = base.EMAIL_HOST_USER
    password = base.EMAIL_HOST_PASSWORD
    tmp = get_name()
    button = get_button()
    template = loader.get_template('users/register.html')
    if request.method == 'POST':
        form = CustomMetCreationForm(request.POST)
        email = request.POST.get("email")
        pwd = request.POST.get("password1")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        app = 'http://localhost/login'
        if form.is_valid():
            user = form.save()
            level = Level.objects.get(id=2)
            profile = Profile(user=user, level=level, description='Meteorólogo')
            profile.save()
            message = 'Meteorólogo registrasdo correctamente'
            tpl = loader.get_template('messages/message.html')
            contextSuccess = {
                'title': get_body(tmp[3], tmp[0]),
                'uri': get_url('users'),
                'message': message,
            }
            message = """Subject: Credenciales para acceder al sistema

                Hola {first_name} {last_name},
                Estas son tus credenciales para acceder al sistema:
                Link: {app}
                Usuario: {email},
                Contraseña: {pwd}

                """
            with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                connection.starttls()  # Construyendo una coneccion segura
                connection.login(user=my_email, password=password)
                connection.sendmail(
                    my_email,
                    email,
                    message.format(first_name=first_name,last_name=last_name, app=app,
                    email=email,pwd=pwd).encode('utf-8')
                )
                connection.quit()
            return HttpResponse(tpl.render(contextSuccess, request))
    else:
        form = CustomMetCreationForm()
    context = {
        'title': get_body(tmp[0], tmp[0]),
        'form': form,
        'uri': get_url('users'),
        'button': button[1],
    }
    return HttpResponse(template.render(context, request))

@login_required()
def edit_met(request, pk):
    my_email = base.EMAIL_HOST_USER
    password = base.EMAIL_HOST_PASSWORD
    tmp = get_name()
    button = get_button()
    template = loader.get_template('users/register.html')
    ins = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = CustomMetCreationForm(request.POST, instance=ins)
        email = request.POST.get("email")
        pwd = request.POST.get("password1")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        app = 'http://localhost/login'
        if form.is_valid():
            form.save()
            message = 'Se enviaron las credenciales'
            tpl = loader.get_template('messages/message.html')
            contextSuccess = {
                'title': get_body(tmp[3], tmp[0]),
                'uri': get_url('users'),
                'message': message,
            }
            message = """Subject: Credenciales para acceder al sistema

                Hola {first_name} {last_name},
                Estas son tus credenciales para acceder al sistema:
                Link: {app}
                Usuario: {email},
                Contraseña: {pwd}

                """
            with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                connection.starttls()  # Construyendo una coneccion segura
                connection.login(user=my_email, password=password)
                connection.sendmail(
                    my_email,
                    email,
                    message.format(first_name=first_name,last_name=last_name, app=app,
                    email=email,pwd=pwd).encode('utf-8')
                )
                connection.quit()
            return HttpResponse(tpl.render(contextSuccess, request))
    else:
        form = CustomMetCreationForm(instance=ins)
    context = {
        'title': get_body(tmp[0], tmp[0]),
        'form': form,
        'uri': get_url('users'),
        'button': button[1],
    }
    return HttpResponse(template.render(context, request))