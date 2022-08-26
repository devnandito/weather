from weather.users.models import User
from datetime import datetime, timedelta

def get_url(url):
    uri = {
        'show': url+':show',
        'create': url+':create',
        'edit': url+':edit',
        'delete': url+':delete',
        'update': url+':update',
        'set': url+':set',
        'editmet': url+':editmet',
        'change': url+':change',
        'showprofile': url+':showprofile',
        'createprofile': url+':createprofile',
        'editprofile': url+':editprofile',
        'deleteprofile': url+':deleteprofile',
        'home': url+':home',
        'print': url+':print',
        'sent': url+':sent',
        'search': url+':search',
        'result': url+':result',
        'dashboard': ':tablero',
        'report': url+':report',
        'storm': url+':storm',
    }
    return uri

def get_body(singular, plural):
    title = {
        'show': 'Administrar '+plural,
        'create': 'Agregar '+singular,
        'edit': 'Editar '+singular,
        'delete': 'Borrar '+singular,
        'change': 'Cambiar '+singular,
        'subtitle': 'Panel de control',
        'login': 'Ingresar al sistema',
        'home': 'Tablero',
        'dashboard': 'Tablero',
        'report': 'Reports',
        'page': 'Principal',
        'search': 'Buscar '+singular,
        'predict': 'Predecir '+singular,
    }
    return title

def get_button():
    button = ['Enviar', 'Guardar', 'Buscar', 'Borrar']
    return button

def get_user(user):
    usr = User.objects.get(username=user)
    return usr

def get_date():
    now = datetime.now()
    return now
