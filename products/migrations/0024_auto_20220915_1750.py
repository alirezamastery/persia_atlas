# Generated by Django 3.2.8 on 2022-09-15 13:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0023_auto_20220915_1746'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProductTypeSelectorValue',
            new_name='VariantSelector',
        ),
        migrations.RenameModel(
            old_name='ProductTypeSelector',
            new_name='VariantSelectorType',
        ),
    ]