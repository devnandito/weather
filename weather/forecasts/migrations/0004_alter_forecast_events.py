# Generated by Django 4.0.5 on 2022-08-13 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forecasts', '0003_forecast_end_forecast_start'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forecast',
            name='events',
            field=models.TextField(blank=True, null=True),
        ),
    ]
