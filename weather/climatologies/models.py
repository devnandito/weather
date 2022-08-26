"""Climatologies models. """

# Django
from django.db import models

# Utilities
from weather.utils.models import CustomModel

# Models
from weather.locations.models import Location
from weather.stations.models import Station
from weather.stationtypes.models import StationType

class Climatology(CustomModel):
    """Climatologies model."""
    id_estacion = models.ForeignKey(
        Location,
        on_delete=models.CASCADE
    )
    station = models.ForeignKey(
        Station,
        on_delete=models.CASCADE
    )
    id_tipo = models.ForeignKey(
        StationType,
        on_delete=models.CASCADE
    )
    nombre_estacion = models.CharField(max_length=60, blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    tmax = models.CharField(max_length=10, blank=True, null=True)
    tmin = models.CharField(max_length=10, blank=True, null=True)
    tmed = models.CharField(max_length=10, blank=True, null=True)
    td = models.CharField(max_length=10, blank=True, null=True)
    pres_est = models.CharField(max_length=10, blank=True, null=True)
    pres_mar = models.CharField(max_length=10, blank=True, null=True)
    prcp = models.CharField(max_length=10, blank=True, null=True)
    hr = models.CharField(max_length=10, blank=True, null=True)
    helio = models.CharField(max_length=10, blank=True, null=True)
    nub = models.CharField(max_length=10, blank=True, null=True)
    vmax_d = models.CharField(max_length=10, blank=True, null=True)
    vmax_f = models.CharField(max_length=10, blank=True, null=True)
    vmed = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.id_estacion.nombre