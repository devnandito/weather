from django.urls import path
from weather.cities.views import show_city, create_city, edit_city, delete_city

app_name = 'weather.cities'

urlpatterns = [
    path('dashboard/create/city', create_city, name='create'),
    path('dashboard/edit/<int:pk>/city', edit_city, name='edit'),
    path('dashboard/delete/<int:pk>/city', delete_city, name='delete'),
    path('dashboard/show/city', show_city, name='show'),
]