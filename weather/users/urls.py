from django.urls import path
from weather.users.views import dashboard, show_user, create_user, edit_user, delete_user, set_pwd, change_pwd, show_profile, create_profile, delete_profile, edit_profile, create_met, show_met, edit_met
app_name = 'weather.users'

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/users/', show_user, name='show'),
    path('dashboard/create/user/', create_user, name='create'),
    path('dashboard/create/user/met', create_met, name='met'),
    path('dashboard/edit/<int:pk>/user', edit_user, name='edit'),
    path('dashboard/delete/<int:pk>/user', delete_user, name='delete'),
    path('dashboard/set/<int:pk>/user', set_pwd, name='set'),
    path('dashboard/change/<int:pk>/user', change_pwd, name='change'),
    path('dashboard/create/user/profile', create_profile, name='createprofile'),
    path('dashboard/edit/user/<int:pk>/profile', edit_profile, name='editprofile'),
    path('dashboard/delete/user/<int:pk>/profile', delete_profile, name='deleteprofile'),
    path('dashboard/show/user/profile', show_profile, name='showprofile'),
    path('dashboard/edit/user/<int:pk>/profile', edit_profile, name='editprofile'),
    path('dashboard/users/met', show_met, name='showmet'),
    path('dashboard/edit/<int:pk>/met', edit_met, name='editmet'),
]