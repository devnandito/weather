"""Forecasts models."""

# Django
from django.db import models

# Models

# Utilities
from weather.utils.models import CustomModel

class Forecast(CustomModel):
    """Forecasts model.

    A forecast
    """

    city = models.CharField(null=True, blank=True, max_length=255)
    temperature = models.CharField(null=True, blank=True, max_length=255)
    feels_like = models.CharField(null=True, blank=True, max_length=255)
    wind = models.CharField(null=True, blank=True, max_length=255)
    pressure = models.CharField(null=True, blank=True, max_length=255)
    humidity = models.CharField(null=True, blank=True, max_length=255)
    comment = models.TextField(null=True, blank=True)
    sender_name = models.CharField(null=True, blank=True, max_length=255)
    alerts = models.TextField(null=True, blank=True)
    events = models.TextField(null=True, blank=True)
    start = models.CharField(null=True, blank=True, max_length=255)
    end = models.CharField(null=True, blank=True, max_length=255)
    user = models.CharField(null=True, blank=True, max_length=255)

    def __str__(self):
        return self.city