# Generated by Django 3.2.8 on 2022-02-14 13:50

from django.db import migrations, models


def dkpc_char_to_int(apps, schema_editor):
    ProductVariant = apps.get_model('products', 'ProductVariant')
    db_alias = schema_editor.connection.alias
    variants = ProductVariant.objects.using(db_alias).all()
    for variant in variants:
        variant.dkpc = int(variant.dkpc_old)
        variant.save()


class Migration(migrations.Migration):
    dependencies = [
        ('products', '0020_productvariant_dkpc'),
    ]

    operations = [
        migrations.RunPython(dkpc_char_to_int),
        migrations.AlterField(
            model_name='productvariant',
            name='dkpc',
            field=models.IntegerField(default=0, unique=True),
            preserve_default=False,
        ),
    ]
