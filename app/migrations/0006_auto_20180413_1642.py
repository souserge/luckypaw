# Generated by Django 2.0.4 on 2018-04-13 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20180403_1844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='pet_size',
            field=models.CharField(blank=True, choices=[('Very Small', 'Very Small'), ('Small', 'Small'), ('Medium', 'Medium'), ('Large', 'Large'), ('Very Large', 'Very Large')], max_length=50),
        ),
    ]
