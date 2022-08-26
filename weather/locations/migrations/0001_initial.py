# Generated by Django 3.2.14 on 2022-07-18 14:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created.', verbose_name='created_at')),
                ('update_at', models.DateTimeField(auto_now=True, help_text='Date time on which the object was last modified.', verbose_name='update_at')),
                ('lon_gra', models.DecimalField(blank=True, decimal_places=8, max_digits=1000, null=True)),
                ('lon_min', models.DecimalField(blank=True, decimal_places=8, max_digits=1000, null=True)),
                ('lon_seg', models.FloatField(blank=True, null=True)),
                ('lon_hem', models.CharField(blank=True, max_length=1, null=True)),
                ('lat_gra', models.DecimalField(blank=True, decimal_places=8, max_digits=1000, null=True)),
                ('lat_min', models.DecimalField(blank=True, decimal_places=8, max_digits=1000, null=True)),
                ('lat_seg', models.FloatField(blank=True, null=True)),
                ('lat_hem', models.CharField(blank=True, max_length=1, null=True)),
                ('elev', models.DecimalField(blank=True, decimal_places=8, max_digits=1000, null=True)),
                ('lon_dec', models.FloatField(blank=True, null=True)),
                ('lat_dec', models.FloatField(blank=True, null=True)),
                ('id_ciudad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cities.city')),
            ],
            options={
                'ordering': ['-created_at', '-update_at'],
                'get_latest_by': 'created_at',
                'abstract': False,
            },
        ),
    ]