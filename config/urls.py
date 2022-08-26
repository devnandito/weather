"""weather URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from weather.users.forms import EmailValidationOnForgotPassword

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('weather.pages.urls', namespace='pages')),
    path('', include('weather.users.urls', namespace='users')),
    path('', include('weather.levels.urls', namespace='levels')),
    path('', include('weather.forecasts.urls', namespace='forecasts')),
    path('', include('weather.geoapps.urls', namespace='geoapps')),
    path('', include('weather.cities.urls', namespace='cities')),
    path('', include('weather.departments.urls', namespace='departments')),
    path('', include('weather.locations.urls', namespace='locations')),
    path('', include('weather.stations.urls', namespace='stations')),
    path('', include('weather.stationtypes.urls', namespace='stationtypes')),
    path('', include('weather.climatologies.urls', namespace='climatologies')),
    path('', include('weather.audits.urls', namespace='audits')),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='pages/password_reset.html', form_class=EmailValidationOnForgotPassword), name='password_reset'),
    path('reset_password_done/', auth_views.PasswordResetDoneView.as_view(template_name='pages/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='pages/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='pages/password_reset_complete.html'), name='password_reset_complete'),
] 
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns += static('/templates/', document_root=settings.PROJECT_DIR + '/templates/')
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT, show_indexes=True)
# +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, show_indexes=True)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, show_indexes=True)
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT, show_indexes=True)

