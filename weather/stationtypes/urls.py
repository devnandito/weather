from django.urls import path
from weather.stationtypes.views import show_station_type, create_station_type, edit_station_type, delete_station_type

app_name = 'weather.cities'

urlpatterns = [
    path('dashboard/create/stationtype', create_station_type, name='create'),
    path('dashboard/edit/<int:pk>/stationtype', edit_station_type, name='edit'),
    path('dashboard/delete/<int:pk>/stationtype', delete_station_type, name='delete'),
    path('dashboard/show/stationtype', show_station_type, name='show'),
]