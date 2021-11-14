from pprint import pprint

import pandas as pd
from django.core.management import BaseCommand

from products.models import Invoice, InvoiceItem, ProductVariant


class Command(BaseCommand):

    def handle(self, *args, **options):
        invoices = Invoice.objects.all()
        dfs = []
        for invoice in invoices:
            print(invoice.pk)
            df = self.calculate_quantities(invoice)
            dfs.append(df)
        overview = pd.concat(dfs)
        overview.set_index(['date', 'name'], inplace=True)
        print(overview)
        overview.to_excel('quantity.xlsx', sheet_name='products')

    @staticmethod
    def calculate_quantities(invoice_obj: Invoice):
        items = InvoiceItem.objects.filter(invoice=invoice_obj)
        dkp_data = {}
        serials = []

        for item in items:
            if item.serial in serials:
                continue
            variant = ProductVariant.objects.select_related('product').get(dkpc=item.dkpc)
            dkp = variant.product.dkp
            if dkp in dkp_data:
                dkp_data[dkp]['count'] += 1
            else:
                dkp_data[dkp] = {
                    'count': 1,
                    'name':  variant.product.title
                }

            serials.append(item.serial)
        pprint(dkp_data)
        names = []
        quantities = []
        for q in dkp_data.values():
            names.append(q['name'])
            quantities.append(q['count'])
        df = pd.DataFrame({'name': names, 'quantity': quantities})
        df['date'] = f'{invoice_obj.start_date} - {invoice_obj.end_date}'
        print(df)
        return df
