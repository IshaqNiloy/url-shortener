# Generated by Django 5.0.6 on 2024-05-26 07:59

import minify.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('minify', '0002_alter_urlmapping_last_visit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='urlmapping',
            name='long_url',
            field=models.URLField(max_length=10000, validators=[minify.models.validate_url]),
        ),
    ]