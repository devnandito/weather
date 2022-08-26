from django.urls import path
from weather.forecasts.views import edit_forecast, result_clima, search_city, sent_email, show_forecast, create_forecast, edit_forecast, delete_forecast, forecast_pdf, predict_forecast, storm_pdf

app_name = 'weather.levels'

urlpatterns = [
    path('dashboard/result/forecast', result_clima, name='result'),
    path('dashboard/search/forecast', search_city, name='search'),
    path('dashboard/sent/forecast', sent_email, name='sent'),
    path('dashboard/create/forecast', create_forecast, name='create'),
    path('dashboard/edit/<int:pk>/forecast', edit_forecast, name='edit'),
    path('dashboard/delete/<int:pk>/forecast', delete_forecast, name='delete'),
    path('dashboard/show/forecast', show_forecast, name='show'),
    path('dashboard/predict/forecast', predict_forecast, name='predict'),
    path('dashboard/report/<int:pk>/forecast', forecast_pdf, name='report'),
    path('dashboard/storm/<int:pk>/forecast', storm_pdf, name='storm'),
]