from django.urls import path
from weather.stations.views import show_station, create_station, edit_station, delete_station

app_name = 'weather.cities'

urlpatterns = [
    path('dashboard/create/station', create_station, name='create'),
    path('dashboard/edit/<int:pk>/station', edit_station, name='edit'),
    path('dashboard/delete/<int:pk>/station', delete_station, name='delete'),
    path('dashboard/show/station', show_station, name='show'),
]