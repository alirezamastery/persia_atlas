# Generated by Django 3.2.8 on 2022-02-04 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_productvariant_stop_loss'),
    ]

    operations = [
        migrations.AddField(
            model_name='producttypeselectorvalue',
            name='extra_info',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
