# Generated by Django 3.2.8 on 2022-02-08 15:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_auto_20220207_1928'),
    ]

    database_operations = [
        migrations.AlterModelTable('Invoice', 'accounting_invoice'),
        migrations.AlterModelTable('InvoiceItem', 'accounting_invoiceitem'),
    ]

    state_operations = [
        migrations.DeleteModel('Invoice'),
        migrations.DeleteModel('InvoiceItem'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=database_operations,
            state_operations=state_operations
        )
    ]
