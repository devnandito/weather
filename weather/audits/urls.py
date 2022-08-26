from django.urls import path
from weather.audits.views import show_audit, audit_pdf
app_name = 'weather.audits'

urlpatterns = [
    path('dashboard/show/audit', show_audit, name='show'),
    path('dashboard/report/<int:pk>/audit', audit_pdf, name='report'),
]