# Generated by Django 3.2.14 on 2022-07-18 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created.', verbose_name='created_at')),
                ('update_at', models.DateTimeField(auto_now=True, help_text='Date time on which the object was last modified.', verbose_name='update_at')),
                ('nombre_dpto', models.CharField(max_length=100)),
                ('nombre_cap', models.CharField(max_length=60)),
            ],
            options={
                'ordering': ['-created_at', '-update_at'],
                'get_latest_by': 'created_at',
                'abstract': False,
            },
        ),
    ]