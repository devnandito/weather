from django.urls import path
from weather.locations.views import show_location, create_location, edit_location, delete_location

app_name = 'weather.locations'

urlpatterns = [
    path('dashboard/create/location', create_location, name='create'),
    path('dashboard/edit/<int:pk>/location', edit_location, name='edit'),
    path('dashboard/delete/<int:pk>/location', delete_location, name='delete'),
    path('dashboard/show/location', show_location, name='show'),
]