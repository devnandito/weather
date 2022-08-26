# coding=utf-8

# Django
from posixpath import split
import profile
from pydoc import describe
from webbrowser import get
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.template import loader
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Models
from weather.levels.models import Level
from weather.users.models import Profile, User

# Forms
from weather.users.forms import CustomNewsCreationForm, FormUnsuscribed

# Utilities
from weather.utils.functions import get_url, get_body, get_button

# Python
import datetime

def get_name():
    name = ['Arasunu Weather']
    return name

def show_home(request):
    template = loader.get_template('pages/show.html')
    tmp = get_name()

    context = {
        'title': get_body(tmp[0], tmp[0]),
    }
    return HttpResponse(template.render(context, request))

def login_user(request):
    tmp = get_name()
    template = loader.get_template('pages/login.html')
    if not request.user.is_anonymous:
        return HttpResponseRedirect(reverse('users:dashboard'))
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                profile = Profile.objects.get(user=user.id)
                profile.last_login = datetime.datetime.now()
                profile.save()
                return HttpResponseRedirect(reverse('users:dashboard'))
            else:
                form = AuthenticationForm()
                text = 'El usuario esta inactivo'
                contextNoActive = {
                    'title': get_body(tmp[0], tmp[0]),
                    'text': text,
                    'form': form,
                }
                return HttpResponse(template.render(contextNoActive, request))
        else:
            form = AuthenticationForm()
            text = 'El usuario o la contraseña son incorrectas'
            contextNoUser = {
                'title': get_body(tmp[0], tmp[0]),
                'text': text,
                'form': form,
            }
            return HttpResponse(template.render(contextNoUser, request))
    else:
        form = AuthenticationForm()
    text = ''
    context = {
        'title': get_body(tmp[0], tmp[0]),
        'form': form,
        'text': text,
    }
    return HttpResponse(template.render(context, request))

@login_required()
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('pages:login'))

def newsletter_user(request):
    tmp = get_name()
    button = get_button()
    template = loader.get_template('pages/register.html')
    if request.method == 'POST':
        form = CustomNewsCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            level = Level.objects.get(id=3)
            profile = Profile(user=user, level=level, description='Newsletter')
            profile.save()
            message = 'Te registraste correctamente'
            tpl = loader.get_template('messages/registermessage.html')
            contextSuccess = {
                'title': get_body(tmp[0], tmp[0]),
                'uri': get_url('geoapps'),
                'message': message,
            }
            return HttpResponse(tpl.render(contextSuccess, request))
    else:
        form = CustomNewsCreationForm()
    context = {
        'title': get_body(tmp[0], tmp[0]),
        'form': form,
        'uri': get_url('users'),
        'button': button[1],
    }
    return HttpResponse(template.render(context, request))

def unsuscribed_user(request):
    tmp = get_name()
    button = get_button()
    template = loader.get_template('users/form.html')
    if request.method == 'POST':
        email = request.POST.get("email")
        if not User.objects.filter(email__iexact=email, profile__level__id=3).exists():
            form = FormUnsuscribed()
            message = "El email no existe"
            context = {
                'title': get_body(tmp[0], tmp[0]),
                'button': button[3],
                'form': form,
                'message': message,
            }
            return HttpResponse(template.render(context, request))
        object_list = User.objects.get(email=email)
        object_list.delete()
        message = 'Se ha cancelado su suscripción'
        tpl = loader.get_template('messages/unsuscribed.html')
        contextSuccess = {
            'title': get_body(tmp[0], tmp[0]),
            'uri': get_url('geoapps'),
            'message': message,
        }
        return HttpResponse(tpl.render(contextSuccess, request))
    else:
        form = FormUnsuscribed()
        context = {
            'title': get_body(tmp[0], tmp[0]),
            'button': button[3],
            'form': form,
        }
    return HttpResponse(template.render(context, request))

# def reset_pwd(request):
#     tmp = get_name()
#     button = get_button()
#     template = loader.get_template('pages/reset.html')
#     context = {
#         'title': get_body(tmp[0], tmp[0]),
#         'button': button[0]
#     }
#     return HttpResponse(template.render(context, request))