# Generated by Django 3.2.8 on 2022-02-07 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_producttype_selector'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='price_step',
        ),
        migrations.AddField(
            model_name='actualproduct',
            name='price_step',
            field=models.IntegerField(default=500),
        ),
    ]
