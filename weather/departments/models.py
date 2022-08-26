"""Departments models. """

# Django
from django.db import models

# Utilities
from weather.utils.models import CustomModel


class Department(CustomModel):
    """Department model."""
    nombre_dpto = models.CharField(max_length=100, blank=False, null=False)
    nombre_cap = models.CharField(max_length=60, blank=False, null=False)

    def __str__(self):
        return self.nombre_dpto