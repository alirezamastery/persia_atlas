from django.db import models


class Product(models.Model):
    dkp = models.CharField(max_length=256, unique=True, blank=False, null=False)
    title = models.CharField(max_length=256)
    is_active = models.BooleanField(default=True, null=False, blank=False)
    type = models.ForeignKey('ProductType', on_delete=models.PROTECT, related_name='products')

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


class ActualProduct(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.title}'
