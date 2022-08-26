from django.urls import path
from weather.departments.views import show_department, create_department, edit_department, delete_department

app_name = 'weather.cities'

urlpatterns = [
    path('dashboard/create/department', create_department, name='create'),
    path('dashboard/edit/<int:pk>/department', edit_department, name='edit'),
    path('dashboard/delete/<int:pk>/department', delete_department, name='delete'),
    path('dashboard/show/department', show_department, name='show'),
]