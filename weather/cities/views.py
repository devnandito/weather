# coding=utf-8

# Django
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage

# Models
from weather.cities.models import City

# Forms
from weather.cities.forms import CityForm

# Utilities
from weather.utils.functions import get_url, get_body, get_button

def get_name():
    name = ['Ciudades', 'ciudades', 'Ciudad', 'ciudad']
    return name

@login_required()
def show_city(request):
    tmp = get_name()
    list_title = ['#', 'Descripción', 'Acciones']
    template = loader.get_template('cities/show.html')
    list_paginator = City.objects.all().order_by("nombre")
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
        'uri': get_url('cities'),
        'list_title': list_title,
    }
    return HttpResponse(template.render(context, request))

@login_required()
def create_city(request):
    tmp = get_name()
    button = get_button()
    template = loader.get_template('cities/add.html')
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
            message = 'Los datos se guardaron correctamente!'
            tpl = loader.get_template('messages/message.html')
            contextSuccess = {
                'title': get_body(tmp[3], tmp[0]),
                'uri': get_url('cities'),
                'message': message,
            }
            return HttpResponse(tpl.render(contextSuccess, request))
    else:
        form = CityForm()
    context = {
        'title': get_body(tmp[3], tmp[0]),
        'form': form,
        'uri': get_url('cities'),
        'button': button[1],
    }
    return HttpResponse(template.render(context, request))

@login_required()
def edit_city(request, pk):
    tmp = get_name()
    button = get_button()
    template = loader.get_template('cities/edit.html')
    ins = get_object_or_404(City, pk=pk)
    if request.method == 'POST':
        form = CityForm(request.POST, instance=ins)
        if form.is_valid():
            form.save()
            message = 'Los datos se guardaron correctamente!'
            tpl = loader.get_template('messages/message.html')
            contextSuccess = {
                'title': get_body(tmp[3], tmp[0]),
                'uri': get_url('cities'),
                'message': message,
            }
            return HttpResponse(tpl.render(contextSuccess, request))
    else:
        form = CityForm(instance=ins)
    context = {
        'title': get_body(tmp[3], tmp[0]),
        'form': form,
        'uri': get_url('cities'),
        'button': button[1],
    }
    return HttpResponse(template.render(context, request))

@login_required()
def delete_city(request, pk):
    tmp = get_name()
    button = get_button()
    template = loader.get_template('cities/delete.html')
    object_list = get_object_or_404(City, pk=pk)
    if request.method == 'POST':
        object_list.delete()
        return HttpResponseRedirect(reverse('cities:show'))
    else:
        context = {
            'title': get_body(tmp[3], tmp[0]),
            'object_list': object_list,
            'uri': get_url('cities'),
            'button': button[3],
        }
    return HttpResponse(template.render(context, request))