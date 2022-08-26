# coding=utf-8

# Django
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage

# Models
from weather.climatologies.models import Climatology

# Forms
from weather.climatologies.forms import ClimatologyForm

# Utilities
from weather.utils.functions import get_url, get_body, get_button

def get_name():
    name = ['Climatologias', 'climatologias', 'Climatologia', 'climatologia']
    return name

@login_required()
def show_climatology(request):
    tmp = get_name()
    list_title = ['#', 'Nombre', 'Fecha', 'Temp Max', 'Temp Min', 'Temp media', 'Acciones']
    template = loader.get_template('climatologies/show.html')
    list_paginator = Climatology.objects.all()[:10000]
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
        'uri': get_url('climatologies'),
        'list_title': list_title,
    }
    return HttpResponse(template.render(context, request))

@login_required()
def create_climatology(request):
    tmp = get_name()
    button = get_button()
    template = loader.get_template('climatologies/add.html')
    if request.method == 'POST':
        form = ClimatologyForm(request.POST)
        if form.is_valid():
            form.save()
            message = 'Los datos se guardaron correctamente!'
            tpl = loader.get_template('messages/message.html')
            contextSuccess = {
                'title': get_body(tmp[3], tmp[0]),
                'uri': get_url('climatologies'),
                'message': message,
            }
            return HttpResponse(tpl.render(contextSuccess, request))
    else:
        form = ClimatologyForm()
    context = {
        'title': get_body(tmp[3], tmp[0]),
        'form': form,
        'uri': get_url('climatologies'),
        'button': button[1],
    }
    return HttpResponse(template.render(context, request))

@login_required()
def edit_climatology(request, pk):
    tmp = get_name()
    button = get_button()
    template = loader.get_template('climatologies/edit.html')
    ins = get_object_or_404(Climatology, pk=pk)
    if request.method == 'POST':
        form = ClimatologyForm(request.POST, instance=ins)
        if form.is_valid():
            form.save()
            message = 'Los datos se guardaron correctamente!'
            tpl = loader.get_template('messages/message.html')
            contextSuccess = {
                'title': get_body(tmp[3], tmp[0]),
                'uri': get_url('climatologies'),
                'message': message,
            }
            return HttpResponse(tpl.render(contextSuccess, request))
    else:
        form = ClimatologyForm(instance=ins)
    context = {
        'title': get_body(tmp[3], tmp[0]),
        'form': form,
        'uri': get_url('climatologies'),
        'button': button[1],
    }
    return HttpResponse(template.render(context, request))

@login_required()
def delete_climatology(request, pk):
    tmp = get_name()
    button = get_button()
    template = loader.get_template('climatologies/delete.html')
    object_list = get_object_or_404(Climatology, pk=pk)
    if request.method == 'POST':
        object_list.delete()
        return HttpResponseRedirect(reverse('climatologies:show'))
    else:
        context = {
            'title': get_body(tmp[3], tmp[0]),
            'object_list': object_list,
            'uri': get_url('climatologies'),
            'button': button[3],
        }
    return HttpResponse(template.render(context, request))