# Generated by Django 4.2.7 on 2024-01-17 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionmodel',
            name='transaction_type',
            field=models.IntegerField(choices=[(1, 'Deposit'), (2, 'Return'), (3, 'Borrow'), (4, 'Pending'), (5, 'Completed')]),
        ),
    ]
