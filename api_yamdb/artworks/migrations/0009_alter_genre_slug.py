# Generated by Django 3.2 on 2023-06-06 12:57

import artworks.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artworks', '0008_alter_genre_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genre',
            name='slug',
            field=models.SlugField(),
        ),
    ]
