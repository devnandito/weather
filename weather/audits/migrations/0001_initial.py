# Generated by Django 4.0.5 on 2022-08-14 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Audit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created.', verbose_name='created_at')),
                ('update_at', models.DateTimeField(auto_now=True, help_text='Date time on which the object was last modified.', verbose_name='update_at')),
                ('schema_name', models.TextField()),
                ('table_name', models.TextField()),
                ('user_name', models.TextField()),
                ('action', models.TextField()),
                ('original_data', models.TextField(blank=True, null=True)),
                ('new_data', models.TextField(blank=True, null=True)),
                ('query', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['-created_at', '-update_at'],
                'get_latest_by': 'created_at',
                'abstract': False,
            },
        ),
    ]
