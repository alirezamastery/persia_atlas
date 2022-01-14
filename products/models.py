from django.db import models


class Brand(models.Model):
    title = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.title}'


class ActualProduct(models.Model):
    title = models.CharField(max_length=255, unique=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, related_name='actual_products')

    def __str__(self):
        return f'{self.title}'


class Product(models.Model):
    dkp = models.CharField(max_length=256, unique=True, blank=False, null=False)
    title = models.CharField(max_length=256)
    is_active = models.BooleanField(default=True, null=False, blank=False)
    type = models.ForeignKey('ProductType', on_delete=models.PROTECT, related_name='products')
    price_step = models.IntegerField(default=500)

    def __str__(self):
        return f'{self.title}'


class ProductType(models.Model):
    title = models.CharField(max_length=256)
    selectors = models.ManyToManyField('ProductTypeSelector', related_name='product_types')

    def __str__(self):
        return f'{self.title}'


class ProductTypeSelector(models.Model):
    title = models.CharField(max_length=256, unique=True, blank=False, null=False)

    def __str__(self):
        return f'{self.title}'


class ProductTypeSelectorValue(models.Model):
    digikala_id = models.IntegerField(unique=True, blank=False, null=False)
    selector = models.ForeignKey(ProductTypeSelector, on_delete=models.CASCADE)
    value = models.CharField(max_length=256, unique=True, blank=False, null=False)

    def __str__(self):
        return f'{self.selector} - {self.value} - {self.digikala_id}'


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    dkpc = models.CharField(max_length=256, unique=True, blank=False, null=False)
    price_min = models.IntegerField(blank=False, null=False)
    is_active = models.BooleanField(default=True, blank=False, null=False)
    has_competition = models.BooleanField(default=True, blank=False, null=False, editable=False)
    selector_values = models.ManyToManyField(ProductTypeSelectorValue, related_name='variants')
    actual_product = models.ForeignKey('ActualProduct', null=True, on_delete=models.SET_NULL,
                                       related_name='variants')

    def __str__(self):
        return f'{self.dkpc}'


class Invoice(models.Model):
    number = models.IntegerField(unique=True)
    start_date = models.CharField(max_length=255)
    end_date = models.CharField(max_length=255)


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT)

    row_number = models.IntegerField()
    code = models.IntegerField()
    date_persian = models.CharField(max_length=255)
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
