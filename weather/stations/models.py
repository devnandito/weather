"""Stations models. """

# Django
from django.db import models

# Utilities
from weather.utils.models import CustomModel

# Models
from weather.locations.models import Location
from weather.stationtypes.models import StationType

class Station(CustomModel):
    """StationType model."""
    name = models.CharField(max_length=240, blank=True, null=True)
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE
    )
    fktypestation = models.ForeignKey(
        StationType,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name