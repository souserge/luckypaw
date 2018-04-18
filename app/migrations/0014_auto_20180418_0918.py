# Generated by Django 2.0.4 on 2018-04-18 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_pet_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pet',
            old_name='description',
            new_name='pet_description',
        ),
        migrations.AlterField(
            model_name='pet',
            name='pet_photo',
            field=models.ImageField(default='images/default_photo.jpg', upload_to='images'),
        ),
        migrations.AlterField(
            model_name='picture',
            name='picture',
            field=models.ImageField(default='images/default_photo.jpg', upload_to='images'),
        ),
        migrations.AlterField(
            model_name='supervisor',
            name='super_photo',
            field=models.ImageField(default='images/default_photo.jpg', upload_to='images'),
        ),
    ]
