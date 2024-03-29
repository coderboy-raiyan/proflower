# Generated by Django 4.2.7 on 2024-01-17 09:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_id', models.IntegerField(unique=True)),
                ('phone_no', models.CharField(max_length=100)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')])),
                ('street_address', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='customer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
