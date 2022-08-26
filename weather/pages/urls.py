from django.urls import path
from weather.pages.views import login_user, logout_user, newsletter_user, unsuscribed_user

app_name = 'weather.pages'

urlpatterns = [
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name="logout"),
    path('register/', newsletter_user, name="register"),
    path('unsuscribed/', unsuscribed_user, name="unsuscribed"),
]