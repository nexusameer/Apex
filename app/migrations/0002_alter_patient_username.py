# Generated by Django 5.2.4 on 2025-07-25 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='username',
            field=models.CharField(blank=True, max_length=150, unique=True),
        ),
    ]
