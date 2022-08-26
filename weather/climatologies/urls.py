from django.urls import path
from weather.climatologies.views import show_climatology, create_climatology, edit_climatology, delete_climatology

app_name = 'weather.cities'

urlpatterns = [
    path('dashboard/create/climatology', create_climatology, name='create'),
    path('dashboard/edit/<int:pk>/climatology', edit_climatology, name='edit'),
    path('dashboard/delete/<int:pk>/climatology', delete_climatology, name='delete'),
    path('dashboard/show/climatology', show_climatology, name='show'),
]