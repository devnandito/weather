"""Audits models. """

# Django
from django.db import models

# Utilities
from weather.utils.models import CustomModel

class Audit(CustomModel):
    """Audit model."""

    schema_name = models.TextField(blank=False, null=False)
    table_name = models.TextField(blank=False, null=False)
    user_name = models.TextField(blank=False, null=False)
    action = models.TextField(blank=False, null=False)
    original_data = models.TextField(blank=True, null=True)
    new_data = models.TextField(blank=True, null=True)
    query = models.TextField(blank=True, null=False)

    def __str__(self):
        return self.user_name