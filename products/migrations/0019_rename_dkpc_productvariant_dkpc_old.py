# Generated by Django 3.2.8 on 2022-02-14 13:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0018_auto_20220208_1854'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productvariant',
            old_name='dkpc',
            new_name='dkpc_old',
        ),
    ]
