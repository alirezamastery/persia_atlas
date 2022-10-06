# Generated by Django 3.2.8 on 2022-10-06 16:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0025_auto_20220915_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producttype',
            name='selector_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='product_types', to='products.variantselectortype'),
            preserve_default=False,
        ),
    ]
