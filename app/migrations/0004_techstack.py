# Generated by Django 3.1.6 on 2021-02-07 06:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20210205_2314'),
    ]

    operations = [
        migrations.CreateModel(
            name='TechStack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', models.ImageField(upload_to='app/images/techstack/icons')),
                ('name', models.CharField(max_length=255)),
                ('link', models.TextField(blank=True, null=True)),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.app')),
            ],
        ),
    ]