# Generated by Django 4.2.7 on 2024-01-17 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flowers', '0002_reviewmodel_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviewmodel',
            name='quantity',
        ),
        migrations.AddField(
            model_name='flowermodel',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]
