# Generated by Django 2.0.4 on 2018-04-19 12:26

import app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_auto_20180419_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='photo',
            field=models.ImageField(default='pets/pet_default_image.jpg', upload_to=app.models.pet_directory_path),
        ),
        migrations.AlterField(
            model_name='picture',
            name='picture',
            field=models.ImageField(default='pets/pet_default_image.jpg', upload_to=app.models.pet_directory_path),
        ),
        migrations.AlterField(
            model_name='supervisor',
            name='super_photo',
            field=models.ImageField(default='users/user_default_image.jpg', upload_to=app.models.user_directory_path),
        ),
    ]