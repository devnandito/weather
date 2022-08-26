# coding=utf-8

# Django
from calendar import month
import encodings
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from numpy import e

# Models
from weather.locations.models import Location
from weather.climatologies.models import Climatology


# Utilities
import os, folium, requests, json
from weather.utils.functions import get_url, get_body, get_button
from config.settings import base


def get_name():
    name = ['Geoapps', 'geoapps', 'Geoapp', 'geoapp']
    return name

# Create your views here.
def show_geoapp(request):
    tmp = get_name()
    template = loader.get_template('geoapps/home1.html')
    shp_dir = os.path.join(os.getcwd(),'media','shp')

    # folium
    m = folium.Map(location=[-25.3080,-57.5629],zoom_start=8)

    ## style
    style_basin = {'fillColor': '#228B22', 'color': '#228B22'}
    style_rivers = { 'color': 'blue'}
    style_cities = { 'color': 'red'}

    ## adding to view
    folium.GeoJson(os.path.join(shp_dir,'basin.geojson'),name='basin',style_function=lambda x:style_basin).add_to(m)
    folium.GeoJson(os.path.join(shp_dir,'estaciones.geojson'),name='estaciones',style_function=lambda x:style_rivers).add_to(m)
    # folium.GeoJson(os.path.join(shp_dir,'Hidrografia_Asuncion.geojson'),style_function=lambda x:style_rivers).add_to(m)
    folium.GeoJson(os.path.join(shp_dir,'Barrios_Localidades_Asuncion.geojson'),style_function=lambda x:style_rivers).add_to(m)
    # folium.GeoJson(os.path.join(shp_dir,'output.json'),style_function=lambda x:style_rivers).add_to(m)
    folium.LayerControl().add_to(m)

    ## exporting
    m=m._repr_html_()
    context = {
        'title': get_body(tmp[3], tmp[0]),
        'uri': get_url('geoapps'),
        'my_map': m,
    }

    ## rendering
    return HttpResponse(template.render(context, request))

def show_goeadmin(request):
    tmp = get_name()
    template = loader.get_template('geoapps/show.html')
    shp_dir = os.path.join(os.getcwd(),'media','shp')

    # folium
    m = folium.Map(location=[-25.3080,-57.5629],zoom_start=12)

    ## style
    style_basin = {'fillColor': '#228B22', 'color': '#228B22'}
    style_rivers = { 'color': 'blue'}
    style_cities = { 'color': 'red'}

    ## adding to view
    folium.GeoJson(os.path.join(shp_dir,'basin.geojson'),name='basin',style_function=lambda x:style_basin).add_to(m)
    folium.GeoJson(os.path.join(shp_dir,'estaciones.geojson'),name='estaciones',style_function=lambda x:style_rivers).add_to(m)
    # folium.GeoJson(os.path.join(shp_dir,'Hidrografia_Asuncion.geojson'),style_function=lambda x:style_rivers).add_to(m)
    folium.GeoJson(os.path.join(shp_dir,'Barrios_Localidades_Asuncion.geojson'),style_function=lambda x:style_rivers).add_to(m)
    # folium.GeoJson(os.path.join(shp_dir,'output.json'),style_function=lambda x:style_rivers).add_to(m)
    folium.LayerControl().add_to(m)

    ## exporting
    m=m._repr_html_()
    context = {
        'title': get_body(tmp[3], tmp[0]),
        'uri': get_url('geoapps'),
        'my_map': m,
    }

    ## rendering
    return HttpResponse(template.render(context, request))

def show_api_v1(request):
    api_key = base.API_KEY
    city = 'Asuncion'
    uri ='http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID='+ api_key
    url =  uri.format(city)
    data = requests.get(url).json()
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type="application/json")

def show_api_v2(request):
    api_key = base.API_KEY
    lat = '-25.263741'
    lon = '-57.575928'
    # uri ='http://api.openweathermap.org/data/2.5/forecast?&units=metric&lat={}&lon={}&appid='+ api_key
    uri ='http://api.openweathermap.org/data/2.5/onecall?&units=metric&exclude=hourly,minutely&lang=sp&lat={}&lon={}&appid='+ api_key
    # uri ='http://api.openweathermap.org/data/2.5/onecall?&units=metric&exclude=minutely&lang=sp&lat={}&lon={}&appid='+ api_key
    url =  uri.format(lat,lon)
    data = requests.get(url).json()
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type="application/json")

def show_api_v3(request):
    api_key = base.API_KEY
    lat = '-25.263741'
    lon = '-57.575928'
    uri ='http://api.openweathermap.org/data/2.5/onecall?&units=metric&exclude=hourly,minutely&lang=sp&lat={}&lon={}&appid='+ api_key
    url =  uri.format(lat,lon)
    data = requests.get(url).json()
    return JsonResponse({'data': data}, status=200)

@csrf_exempt
def show_api_history(request):
    city = request.GET.get('city')
    month = request.GET.get('month')
    year = request.GET.get('year')
    object_list = Climatology.objects.filter(
        id_estacion_id__id_ciudad__nombre__icontains=city,
        fecha__month=int(month),
        fecha__year=int(year)
    ).order_by('fecha')
    data = [{'date': item.fecha.day, 'tmax': item.tmax, 'tmin': item.tmin} for item in object_list]

    data_json = json.dumps(data, ensure_ascii=False).encode('utf-8')
    return HttpResponse(data_json, content_type='application/json')

def show_api_station(request):
    object_list = Location.objects.all()
    data = [{'station': item.id_ciudad.nombre} for item in object_list]

    data_json = json.dumps(data, ensure_ascii=False).encode('utf-8')
    return HttpResponse(data_json, content_type='application/json')