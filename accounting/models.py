from django.db import models


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CostType(TimestampedModel):
    title = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.title}'


class Cost(TimestampedModel):
    type = models.ForeignKey(CostType, on_delete=models.PROTECT, related_name='costs')
    amount = models.IntegerField()
    date = models.DateField()
    description = models.TextField(default='', blank=True)

    def __str__(self):
        return f'{self.type}-{self.amount}'


class Income(TimestampedModel):
    amount = models.IntegerField()
    date = models.DateField()
    description = models.TextField(default='', blank=True)

    def __str__(self):
        return f'{self.amount}-{self.date}'


class ProductCost(TimestampedModel):
    amount = models.IntegerField()
    date = models.DateField()
    description = models.TextField(default='', blank=True)

    def __str__(self):
        return f'{self.amount}-{self.date}'


class Invoice(models.Model):
    number = models.IntegerField(unique=True)
    start_date_persian = models.CharField(max_length=255)
    end_date_persian = models.CharField(max_length=255)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.PROTECT,
        related_name='invoice_items'
    )

    row_number = models.IntegerField()
    code = models.IntegerField()

    date_persian = models.CharField(max_length=255)
    date = models.DateTimeField(blank=True, null=True)

    dkpc = models.IntegerField()
    variant_title = models.CharField(max_length=255)
    order_id = models.IntegerField()
    serial = models.CharField(max_length=255)
    credit = models.IntegerField()
    debit = models.IntegerField()
    credit_discount = models.IntegerField()
    debit_discount = models.IntegerField()
    credit_final = models.IntegerField()
    debit_final = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    calculated = models.BooleanField(default=False)


__all__ = [
    'CostType',
    'Cost',
    'Income',
    'ProductCost',
    'Invoice',
    'InvoiceItem'
]
