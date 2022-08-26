# coding=utf-8

# Django
from calendar import month
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage

# library pdf
from io import BytesIO, StringIO
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle, Table, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch, landscape, portrait

# Models
from weather.users.models import User

# Forms
from weather.forecasts.forms import FormForecast, FormSearchCity, FormGeo, FormAlert, FormPredict
from weather.forecasts.models import Forecast

# Utilities
from weather.utils.functions import get_url, get_body, get_button, get_user, get_date

# Python
from config.settings import base
import requests, smtplib, csv, os, pytz
from datetime import timedelta, datetime

APPS_DIR = base.APPS_DIR
static = str(APPS_DIR.path('static'))

def get_name():
    name = ['Pronostico', 'pronosticos', 'Pronostico', 'pronostico', 'Ciudad', 'Tormenta']
    return name

@login_required()
def show_forecast(request):
    tmp = get_name()
    list_title = ['#', 'Ciudad', 'Temperatura', 'Termica', 'Humedad', 'Presión',  'Comentario', 'Acciones']
    template = loader.get_template('forecasts/show.html')
    list_paginator = Forecast.objects.all()
    paginator = Paginator(list_paginator, 5)
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
        'uri': get_url('forecasts'),
        'list_title': list_title,
    }
    return HttpResponse(template.render(context, request))

@login_required()
def create_forecast(request):
    tmp = get_name()
    button = get_button()
    template = loader.get_template('forecasts/add.html')
    if request.method == 'POST':
        form = FormAlert(request.POST)
        if form.is_valid():
            form.save()
            message = 'Los datos se guardaron correctamente!'
            tpl = loader.get_template('messages/message.html')
            contextSuccess = {
                'title': get_body(tmp[3], tmp[0]),
                'uri': get_url('forecasts'),
                'message': message,
            }
            return HttpResponse(tpl.render(contextSuccess, request))
    else:
        form = FormAlert()
    context = {
        'title': get_body(tmp[3], tmp[0]),
        'form': form,
        'uri': get_url('forecasts'),
        'button': button[1],
    }
    return HttpResponse(template.render(context, request))

@login_required()
def edit_forecast(request, pk):
    tmp = get_name()
    button = get_button()
    template = loader.get_template('forecasts/edit.html')
    ins = get_object_or_404(Forecast, pk=pk)
    if request.method == 'POST':
        form = FormAlert(request.POST, instance=ins)
        if form.is_valid():
            form.save()
            message = 'Los datos se guardaron correctamente!'
            tpl = loader.get_template('messages/message.html')
            contextSuccess = {
                'title': get_body(tmp[3], tmp[0]),
                'uri': get_url('forecasts'),
                'message': message,
            }
            return HttpResponse(tpl.render(contextSuccess, request))
    else:
        form = FormAlert(instance=ins)
    context = {
        'title': get_body(tmp[3], tmp[0]),
        'form': form,
        'uri': get_url('forecasts'),
        'button': button[1],
    }
    return HttpResponse(template.render(context, request))

@login_required()
def delete_forecast(request, pk):
    tmp = get_name()
    button = get_button()
    template = loader.get_template('forecasts/delete.html')
    object_list = get_object_or_404(Forecast, pk=pk)
    if request.method == 'POST':
        object_list.delete()
        return HttpResponseRedirect(reverse('forecasts:show'))
    else:
        context = {
            'title': get_body(tmp[3], tmp[0]),
            'object_list': object_list,
            'uri': get_url('forecasts'),
            'button': button[3],
        }
    return HttpResponse(template.render(context, request))

@login_required()
def search_city(request):
    # https://api.openweathermap.org/data/2.5/onecall?lat=-25&lon=-57&exclude=hourly,daily&units=metric&Lang=SP&appid=9a33c608af643fd3bf10cb2a2eedaa38
    button = get_button()
    template = loader.get_template('forecasts/search.html')
    tmp = get_name()
    api_key = base.API_KEY
    lats = '-25'
    lons = '-57'
    uri = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=hourly,daily&units=metric&Lang=SP&appid='+ api_key
    url = uri.format(lats, lons)
    data = requests.get(url).json()
    if 'alerts' in data:
        size = len(data['alerts'])
        if size == 1:
            num = 0
        elif size == 3:
            num = 2
        else:
            num = 1
        if data['alerts'][num]['sender_name'].find('DMH-DINAC') !=-1:
            default_data = {
                'city': data['timezone'],
                'lat': lats,
                'lon': lons
            }
            form = FormGeo(initial=default_data)
            flag = 1
        else:
            form = FormSearchCity()
            flag = 2
            num = 0
    else:
        form = FormSearchCity()
        flag = 2
        num = 0

    context = {
        'title': get_body(tmp[4], tmp[4]),
        'form': form,
        'button': button[2],
        'uri': get_url('forecasts'),
        'flag': flag,
        'num': num,
    }
    return HttpResponse(template.render(context, request))

@login_required()
def result_clima(request):
    template = loader.get_template('forecasts/result.html')
    tmp = get_name()
    button = get_button()
    city = request.POST.get("city")
    flag = request.POST.get("flag")
    num = int(request.POST.get("num"))
    lat = request.POST.get("lat")
    lon = request.POST.get("lon")
    api_key = base.API_KEY
    if flag == '1':
        uri = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=hourly,daily&units=metric&Lang=SP&appid='+ api_key
        url = uri.format(lat,lon)
        data = requests.get(url).json()
        current = data['current']
        temperature = current['temp']
        feels_like = current['feels_like']
        humidity = current['humidity']
        pressure = current['pressure']
        wind = current['wind_speed']
        events = data['alerts'][num]['event']
        sender_name = data['alerts'][num]['sender_name']
        alerts = data['alerts'][num]['description']
        start = datetime.fromtimestamp(data['alerts'][num]['start'], pytz.timezone(data['timezone']))
        end = datetime.fromtimestamp(data['alerts'][num]['end'], pytz.timezone(data['timezone']))
        user = request.user
        default_data = {
            'city': city,
            'temperature': temperature,
            'feels_like': feels_like,
            'wind': wind,
            'pressure': pressure,
            'humidity': humidity,
            'events': events,
            'sender_name': sender_name,
            'alerts': alerts,
            'start': start,
            'end': end,
            'user': user,
        }
        form = FormAlert(initial=default_data)
    else:
        uri ='http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID='+ api_key
        url =  uri.format(city)
        data = requests.get(url).json()
        main = data['main']
        temperature = main['temp']
        feels_like = main['feels_like']
        humidity = main['humidity']
        pressure = main['pressure']
        wind = data['wind']['speed']
        default_data = {
            'city': city,
            'temperature': temperature,
            'feels_like': feels_like,
            'wind': wind,
            'pressure': pressure,
            'humidity': humidity,
            'user': request.user,
        }
        form = FormForecast(initial=default_data)
    context = {
        'title': get_body(tmp[3], tmp[0]),
        'form': form,
        'button': button[0],
        'uri': get_url('forecasts'),
        'flag':flag,
    }
    return HttpResponse(template.render(context, request))

@login_required()
def sent_email(request):
    object_list = User.objects.filter(profile__level__id=3)
    city = request.POST.get("city")
    my_email = base.EMAIL_HOST_USER
    password = base.EMAIL_HOST_PASSWORD
    tmp = get_name()
    flag = request.POST.get("flag")
    temperature = request.POST.get("temperature")
    feels_like = request.POST.get("feels_like")
    humidity = request.POST.get("humidity")
    pressure = request.POST.get("pressure")
    event = request.POST.get("events")
    sender_name = request.POST.get("sender_name")
    comment = request.POST.get("comment")
    events = request.POST.get("events")
    alerts = request.POST.get("alerts")
    start = request.POST.get("start")
    end = request.POST.get("end")
    now = datetime.now()
    ihour = now.hour
    iminute = now.minute
    isecond = now.second
    timestart = timedelta(hours = ihour, minutes = iminute, seconds = isecond)
    if flag == '1':
        message1 = """Subject: Alerta Meteorologica

            Hola {grade} {name} en {CITY},
            su temperatura actual es
            de {temperature} grados, \n
            con una sensacion termica {feels_like} \n
            una Humedad relativa de {humidity} %, \n
            una presion de {pressure}hPa \n
            La Alerta vigente "{event}" emitida por {sender_name}
            es la siguiente: \n
            {alerts}
            Comentario del meteorólogo: {comment}, \n
            Inicio: {start}
            Fin: {end}
            Hora: {timestart}

        """
    else:
        message1 = """Subject: Estado Meteorologico

            Hola {grade} {name} en la ciudad de {CITY},
            su temperatura actual es
            de {temperature} grados,
            con una sensacion termica {feels_like}
            una Humedad relativa de {humidity} %,
            una presion de {pressure}hPa,
            Comentario del meteorólogo: {comment},
            Hora: {timestart}

        """
    form = FormAlert(request.POST)
    if form.is_valid():
        form.save()
    # forecast = Forecast(
    #             city=city, temperature=temperature, feels_like=feels_like, 
    #             pressure=pressure, humidity=humidity, comment=comment,
    #             sender_name=sender_name, alerts=alerts,
    #             events = events, start = start, end= end
    #             )
    # forecast.save()
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()  # Construyendo una coneccion segura
        connection.login(user=my_email, password=password)
        for item in object_list:
            connection.sendmail(
                my_email,
                item.email,
                message1.format(CITY=city,temperature=temperature,
                feels_like=feels_like,humidity=humidity,
                pressure=pressure,
                comment=comment,
                timestart=timestart,
                start=start,
                end=end,
                name=item.last_name,grade=item.first_name,
                event=event,sender_name=sender_name,alerts=alerts).encode('utf-8')
            )
        connection.quit()
    template = loader.get_template('messages/message.html')
    message = 'El correo fue enviado'
    context = {
        'title': get_body(tmp[3], tmp[0]),
        'uri': get_url('forecasts'),
        'message': message,
    }
    return HttpResponse(template.render(context, request))

@login_required()
def predict_forecast(request):
    tmp = get_name()
    button = get_button()
    template = loader.get_template('forecasts/predict.html')
    if request.method == 'POST':
        temp = request.POST.get("temperature")
        pressure = request.POST.get("pressure")
        humidity = request.POST.get("humidity")
        try:
            object_list = Forecast.objects.filter(temperature__icontains=temp, pressure__contains=pressure, humidity__contains=humidity)
            message = 'Corresponde a una tormenta que tiene las siguientes caracteristicas'
        except Forecast.DoesNotExist:
            message = 'No existe registro de tormentas con esos parametros'

        tpl = loader.get_template('forecasts/storm.html')
        contextSuccess = {
            'title': get_body(tmp[5], tmp[0]),
            'uri': get_url('forecasts'),
            'message': message,
            'object_list': object_list,
        }
        return HttpResponse(tpl.render(contextSuccess, request))
    else:
        form = FormPredict()
    context = {
        'title': get_body(tmp[5], tmp[0]),
        'form': form,
        'uri': get_url('forecasts'),
        'button': button[0],
    }
    return HttpResponse(template.render(context, request))

@login_required()
def forecast_pdf(request, pk):
    now = get_date()
    timestart = now.strftime("%Y-%m-%d %H:%M:%S")
    username = get_user(request.user)
    response = HttpResponse(content_type='aplication/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte.pdf"'
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72,
        pagesize=portrait(letter))
    # Our container for 'Flowable' objects
    elements = []
    logo = static+'/img/pdf/arasunu-small.png'
    im = Image(logo, 1*inch, 0.4*inch)
    # im = Image(logo, 1.9*inch, 0.4*inch, hAlign='LEFT')

    # A large collection of style sheets pre-made for us
    styles = getSampleStyleSheet()
    style_right = ParagraphStyle(name='right', parent=styles['Normal'], alignment=TA_RIGHT)
    style_left = ParagraphStyle(name='left', parent=styles['Normal'], alignment=TA_LEFT)
    title = styles['Heading1']
    title.alignment=TA_CENTER
    text_r = styles["Normal"]
    text_r.alignment=TA_RIGHT
    text_l = styles["BodyText"]
    text_l.alignment=TA_LEFT
    styles.wordWrap = 'CJK'
    styles.add(ParagraphStyle(name='RightAlign', alignment=TA_JUSTIFY))
    user_report = "Generado por: {} \n Fecha: {}".format(username,timestart)
    # date_report = "Fecha: {} ".format(timestart)
    table_data = [
        [im, Paragraph(str(user_report), style_right)],
        # ["", Paragraph(str(date_report), style_right)],
    ]
    # elements.append(im)
    tbl = Table(table_data)
    elements.append(tbl)
    elements.append(Spacer(1, 20))
    elements.append(Paragraph('Pronóstico Meteorológico', title))
    elements.append(Spacer(1, 20))
    object_list = Forecast.objects.filter(pk=pk)
    for item in object_list:
        user = get_user(item.user)
        # Add a row to the table
        city = "CIUDAD: {}".format(item.city)
        temp = "TEMPERATURA: {}".format(item.temperature)
        pressure = "PRESION: {}".format(item.pressure)
        humidity = "HUMEDAD: {}".format(item.humidity)
        sender_name = "ENTIDAD: {}".format(item.sender_name)
        start = "HORA DE INICIO: {}".format(item.start)
        end = "HORA DE FINALIZACION: {}".format(item.end)
        user = "METEOROLOGO RESPONSABLE: {} {}".format(user.first_name, user.last_name)
        elements.append(Paragraph(city, style_left))
        elements.append(Paragraph(str(temp), text_l))
        elements.append(Paragraph(str(pressure), text_l))
        elements.append(Paragraph(str(humidity), text_l))
        elements.append(Paragraph('COMENTARIO', text_l))
        elements.append(Paragraph(str(item.comment), text_l))
        elements.append(Paragraph(str(sender_name), text_l))
        elements.append(Paragraph(str(start), text_l))
        elements.append(Paragraph(str(end), text_l))
        elements.append(Paragraph(str(user), text_l))
    doc.build(elements)

    # Get the value of the BytesIO buffer and write it to the response.
    response.write(buff.getvalue())
    buff.close()
    return response

@login_required()
def storm_pdf(request, pk):
    now = get_date()
    timestart = now.strftime("%Y-%m-%d %H:%M:%S")
    username = get_user(request.user)
    response = HttpResponse(content_type='aplication/pdf')
    response['Content-Disposition'] = 'attachment; filename="storm.pdf"'
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72,
        pagesize=portrait(letter))
    # Our container for 'Flowable' objects
    elements = []
    logo = static+'/img/pdf/arasunu-small.png'
    im = Image(logo, 1*inch, 0.4*inch)
    # im = Image(logo, 1.9*inch, 0.4*inch, hAlign='LEFT')

    # A large collection of style sheets pre-made for us
    styles = getSampleStyleSheet()
    style_right = ParagraphStyle(name='right', parent=styles['Normal'], alignment=TA_RIGHT)
    style_left = ParagraphStyle(name='left', parent=styles['Normal'], alignment=TA_LEFT)
    title = styles['Heading1']
    title.alignment=TA_CENTER
    text_r = styles["Normal"]
    text_r.alignment=TA_RIGHT
    text_l = styles["BodyText"]
    text_l.alignment=TA_LEFT
    styles.wordWrap = 'CJK'
    styles.add(ParagraphStyle(name='RightAlign', alignment=TA_JUSTIFY))
    user_report = "Generado por: {} \n Fecha: {}".format(username,timestart)
    # date_report = "Fecha: {} ".format(timestart)
    table_data = [
        [im, Paragraph(str(user_report), style_right)],
        # ["", Paragraph(str(date_report), style_right)],
    ]
    # elements.append(im)
    tbl = Table(table_data)
    elements.append(tbl)
    elements.append(Spacer(1, 20))
    elements.append(Paragraph('Reporte de Tormenta', title))
    elements.append(Spacer(1, 20))
    object_list = Forecast.objects.filter(pk=pk)
    for item in object_list:
        user = get_user(item.user)
        # Add a row to the table
        city = "CIUDAD: {}".format(item.city)
        temp = "TEMPERATURA: {}".format(item.temperature)
        pressure = "PRESION: {}".format(item.pressure)
        humidity = "HUMEDAD: {}".format(item.humidity)
        sender_name = "ENTIDAD: {}".format(item.sender_name)
        start = "HORA DE INICIO: {}".format(item.start)
        end = "HORA DE FINALIZACION: {}".format(item.end)
        user = "METEOROLOGO RESPONSABLE: {} {}".format(user.first_name, user.last_name)
        elements.append(Paragraph(city, style_left))
        elements.append(Paragraph(str(temp), text_l))
        elements.append(Paragraph(str(pressure), text_l))
        elements.append(Paragraph(str(humidity), text_l))
        elements.append(Paragraph('COMENTARIO', text_l))
        elements.append(Paragraph(str(item.comment), text_l))
        elements.append(Paragraph(str(sender_name), text_l))
        elements.append(Paragraph(str(start), text_l))
        elements.append(Paragraph(str(end), text_l))
        elements.append(Paragraph(str(user), text_l))
    doc.build(elements)

    # Get the value of the BytesIO buffer and write it to the response.
    response.write(buff.getvalue())
    buff.close()
    return response