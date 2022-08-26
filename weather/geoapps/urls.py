from django.urls import path
from weather.geoapps.views import show_geoapp, show_goeadmin, show_api_v1, show_api_v2, show_api_v3, show_api_history, show_api_station

app_name = 'weather.geoapps'

urlpatterns = [
    path('', show_geoapp, name='home'),
    path('dashboard/show/geoapp', show_goeadmin, name='show'),
    path('api/v1', show_api_v1, name='apiv1'),
    path('api/v2', show_api_v2, name='apiv2'),
    path('api/v3', show_api_v3, name='apiv3'),
    path('api/v4', show_api_history, name='history'),
    path('api/v5', show_api_station, name='station'),
]