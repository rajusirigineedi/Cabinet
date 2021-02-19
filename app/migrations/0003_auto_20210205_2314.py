# Generated by Django 3.1.6 on 2021-02-05 17:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20210205_2209'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='app',
            name='images',
        ),
        migrations.CreateModel(
            name='SnapAndDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('screenshot', models.ImageField(upload_to='app/images/appdata/snaps')),
                ('header', models.CharField(max_length=255)),
                ('info', models.TextField()),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.app')),
            ],
        ),
    ]