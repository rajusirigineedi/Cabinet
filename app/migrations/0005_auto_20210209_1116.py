# Generated by Django 3.1.6 on 2021-02-09 05:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_techstack'),
    ]

    operations = [
        migrations.RenameField(
            model_name='app',
            old_name='header_infos',
            new_name='intro',
        ),
        migrations.RemoveField(
            model_name='app',
            name='headers',
        ),
    ]
