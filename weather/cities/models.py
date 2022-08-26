"""Cities models. """

# Django
from django.db import models

# Utilities
from weather.utils.models import CustomModel

# Models
from weather.departments.models import Department

class City(CustomModel):
    """City model."""

    id_dpto = models.ForeignKey(
        Department,
        on_delete=models.CASCADE
    )
    nombre = models.CharField(max_length=140, blank=False, null=False)

    def __str__(self):
        return self.nombre