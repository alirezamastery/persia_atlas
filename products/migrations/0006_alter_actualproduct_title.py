# Generated by Django 3.2.8 on 2021-10-15 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_productvariant_actual_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actualproduct',
            name='title',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
