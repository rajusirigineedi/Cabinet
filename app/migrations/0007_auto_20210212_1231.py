# Generated by Django 3.1.6 on 2021-02-12 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_app_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='app',
            name='start_id',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='snapanddetail',
            name='next_id',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='snapanddetail',
            name='prev_id',
            field=models.IntegerField(default=-1),
        ),
    ]
