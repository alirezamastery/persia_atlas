# Generated by Django 3.2.8 on 2022-01-22 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_auto_20220122_0624'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='invoiceitem',
            name='date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
