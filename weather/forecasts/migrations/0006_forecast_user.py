# Generated by Django 4.0.5 on 2022-08-14 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forecasts', '0005_alter_forecast_alerts'),
    ]

    operations = [
        migrations.AddField(
            model_name='forecast',
            name='user',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]