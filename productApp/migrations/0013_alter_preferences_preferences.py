# Generated by Django 3.2.7 on 2021-09-24 16:25

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productApp', '0012_preferences'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preferences',
            name='preferences',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None),
        ),
    ]
