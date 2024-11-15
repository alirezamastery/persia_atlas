# Generated by Django 3.2.8 on 2021-10-14 15:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_productvariant_has_competition'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActualProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='productvariant',
            name='actual_product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.actualproduct'),
        ),
    ]
