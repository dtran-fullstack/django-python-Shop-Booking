# Generated by Django 2.2 on 2020-09-09 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard_app', '0002_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='services',
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(default='pic_folder/None/no-img.jpg', upload_to='pic_folder/'),
        ),
    ]
