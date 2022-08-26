# coding=utf-8

# Django
from ctypes import alignment
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage

# Models
from weather.audits.models import Audit

# Forms

# library pdf
from io import BytesIO, StringIO
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle, Table, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch, landscape, portrait

# Utilities
from weather.utils.functions import get_url, get_body, get_user, get_date

# Python
from config.settings import base
from datetime import timedelta

APPS_DIR = base.APPS_DIR
static = str(APPS_DIR.path('static'))

def get_name():
    name = ['Auditorias', 'auditorias', 'Auditoria', 'auditoria']
    return name

@login_required()
def show_audit(request):
    tmp = get_name()
    list_title = ['#', 'Tabla', 'Usuario', 'Datos', 'Acción', 'Creación', 'Actualización']
    template = loader.get_template('audits/show.html')
    list_paginator = Audit.objects.all()
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
        'uri': get_url('audits'),
        'list_title': list_title,
    }
    return HttpResponse(template.render(context, request))


@login_required()
def audit_pdf(request, pk):
    now = get_date()
    timestart = now.strftime("%Y-%m-%d %H:%M:%S")
    username = get_user(request.user)
    response = HttpResponse(content_type='aplication/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_auditoria.pdf"'
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72,
        pagesize=portrait(letter))
    # Our container for 'Flowable' objects
    elements = []
    logo = static+'/img/pdf/logo-mini.png'
    im = Image(logo, 0.9*inch, 1.5*inch, hAlign='LEFT')

    # A large collection of style sheets pre-made for us
    styles = getSampleStyleSheet()
    title = styles['Heading1']
    title.alignment=TA_CENTER
    text_r = styles["Normal"]
    text_r.alignment=TA_RIGHT
    text_p = styles["BodyText"]
    text_p.alignment=TA_LEFT
    styles.wordWrap = 'CJK'
    styles.add(ParagraphStyle(name='RightAlign', alignment=TA_JUSTIFY))
    user_report = "Generado por: {}".format(username)
    get_time = "Fecha: {}".format(timestart)
    elements.append(Paragraph(str(user_report), text_r))
    elements.append(Paragraph(str(get_time), text_r))
    elements.append(Spacer(1, 18))
    elements.append(im)

    elements.append(Paragraph('Reporte Auditoria', title))
    elements.append(Spacer(1, 20))
    object_list = Audit.objects.filter(pk=pk)
    for item in object_list:
        # Add a row to the table
        schema = "ESQUEMA: {}".format(item.schema_name)
        table_name = "TABLA: {}".format(item.table_name)
        username = "USUARIO: {}".format(item.user_name)
        action = "ACCION: {}".format(item.action)
        elements.append(Paragraph(schema, text_p))
        elements.append(Paragraph(str(table_name), text_p))
        elements.append(Paragraph(str(username), text_p))
        elements.append(Paragraph(str(action), text_p))
        elements.append(Paragraph('DATOS', text_p))
        elements.append(Paragraph(str(item.original_data), text_p))
    doc.build(elements)

    # Get the value of the BytesIO buffer and write it to the response.
    response.write(buff.getvalue())
    buff.close()
    return response