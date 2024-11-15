# Generated by Django 3.2.8 on 2022-02-08 17:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0002_income_productcost'),
        ('products', '0018_auto_20220208_1854'),
    ]

    state_operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(unique=True)),
                ('start_date_persian', models.CharField(max_length=255)),
                ('end_date_persian', models.CharField(max_length=255)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row_number', models.IntegerField()),
                ('code', models.IntegerField()),
                ('date_persian', models.CharField(max_length=255)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('dkpc', models.IntegerField()),
                ('variant_title', models.CharField(max_length=255)),
                ('order_id', models.IntegerField()),
                ('serial', models.CharField(max_length=255)),
                ('credit', models.IntegerField()),
                ('debit', models.IntegerField()),
                ('credit_discount', models.IntegerField()),
                ('debit_discount', models.IntegerField()),
                ('credit_final', models.IntegerField()),
                ('debit_final', models.IntegerField()),
                ('description', models.TextField(blank=True, null=True)),
                ('calculated', models.BooleanField(default=False)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='invoice_items', to='accounting.invoice')),
            ],
        ),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(state_operations=state_operations)
    ]
