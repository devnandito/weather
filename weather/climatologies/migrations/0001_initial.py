# Generated by Django 3.2.14 on 2022-07-18 14:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stations', '0001_initial'),
        ('stationtypes', '0001_initial'),
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Climatology',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created.', verbose_name='created_at')),
                ('update_at', models.DateTimeField(auto_now=True, help_text='Date time on which the object was last modified.', verbose_name='update_at')),
                ('nombre_estacion', models.CharField(blank=True, max_length=60, null=True)),
                ('fecha', models.DateTimeField(blank=True, null=True)),
                ('tmax', models.CharField(blank=True, max_length=10, null=True)),
                ('tmin', models.CharField(blank=True, max_length=10, null=True)),
                ('tmed', models.CharField(blank=True, max_length=10, null=True)),
                ('td', models.CharField(blank=True, max_length=10, null=True)),
                ('pres_est', models.CharField(blank=True, max_length=10, null=True)),
                ('pres_mar', models.CharField(blank=True, max_length=10, null=True)),
                ('prcp', models.CharField(blank=True, max_length=10, null=True)),
                ('hr', models.CharField(blank=True, max_length=10, null=True)),
                ('helio', models.CharField(blank=True, max_length=10, null=True)),
                ('nub', models.CharField(blank=True, max_length=10, null=True)),
                ('vmax_d', models.CharField(blank=True, max_length=10, null=True)),
                ('vmax_f', models.CharField(blank=True, max_length=10, null=True)),
                ('vmed', models.CharField(blank=True, max_length=10, null=True)),
                ('id_estacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locations.location')),
                ('id_tipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stationtypes.stationtype')),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stations.station')),
            ],
            options={
                'ordering': ['-created_at', '-update_at'],
                'get_latest_by': 'created_at',
                'abstract': False,
            },
        ),
    ]
