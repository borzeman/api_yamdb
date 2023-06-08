# Generated by Django 3.2 on 2023-06-07 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artworks', '0019_alter_title_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(blank=True, related_name='genre', to='artworks.Genre'),
        ),
    ]
