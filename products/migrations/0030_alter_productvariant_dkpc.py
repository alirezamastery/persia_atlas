# Generated by Django 3.2.8 on 2022-10-29 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0029_auto_20221008_2329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productvariant',
            name='dkpc',
            field=models.PositiveBigIntegerField(unique=True),
        ),
    ]
