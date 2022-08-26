"""StationTypes models. """

# Django
from django.db import models

# Utilities
from weather.utils.models import CustomModel


class StationType(CustomModel):
    """StationType model."""
    nombre = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.nombre