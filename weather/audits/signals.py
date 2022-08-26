from django.db.models.signals import post_save
from django.dispatch import receiver

from weather.forecasts.models import Forecast
from weather.audits.models import Audit

@receiver(post_save, sender=Forecast)
def created_audit(sender, instance, created, **kwargs):
    data_format = """
    temperature: {}, feels_like: {}, pressure: {}, 
    humidity: {}, comment: {}, sender_name: {}, 
    alerts: {}, events: {}, start: {}, end: {}
    """
    data = data_format.format(
        instance.temperature, instance.feels_like,
        instance.pressure, instance.humidity,
        instance.comment, instance.sender_name,
        instance.alerts, instance.events,
        instance.start, instance.end
    )

    if created:
        Audit.objects.create(
            schema_name = 'public',
            table_name='Forecast',
            user_name = instance.user,
            action = 'I',
            original_data = data,
        )

@receiver(post_save, sender=Forecast)
def update_audit(sender, instance, created, **kwargs):
    if created == False:
        data_format = """
        temperature: {}, feels_like: {}, pressure: {}, 
        humidity: {}, comment: {}, sender_name: {}, 
        alerts: {}, events: {}, start: {}, end: {}
        """
        data = data_format.format(
            instance.temperature, instance.feels_like,
            instance.pressure, instance.humidity,
            instance.comment, instance.sender_name,
            instance.alerts, instance.events,
            instance.start, instance.end
        )
        audit = Audit(
            schema_name = 'public',
            table_name='Forecast',
            user_name = instance.user,
            action = 'U',
            original_data = data,
        )
        audit.save()