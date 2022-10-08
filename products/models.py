from django.db import models


class Brand(models.Model):
    title = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.title}'


class ActualProduct(models.Model):
    title = models.CharField(max_length=255, unique=True)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='actual_products')
    price_step = models.IntegerField(default=500)

    def __str__(self):
        return f'{self.title}'


class Product(models.Model):
    dkp = models.CharField(max_length=256, unique=True, blank=False, null=False)
    title = models.CharField(max_length=256)
    is_active = models.BooleanField(default=True, null=False, blank=False)
    type = models.ForeignKey('ProductType', on_delete=models.PROTECT, related_name='products')

    def __str__(self):
        return f'{self.title}'


class ProductType(models.Model):
    title = models.CharField(max_length=256)
    selector_type = models.ForeignKey(
        'VariantSelectorType',
        on_delete=models.PROTECT,
        related_name='product_types'
    )

    def __str__(self):
        return f'{self.title}'


class VariantSelectorType(models.Model):
    title = models.CharField(max_length=256, unique=True, blank=False, null=False)

    def __str__(self):
        return f'{self.title}'


class VariantSelector(models.Model):
    digikala_id = models.IntegerField(unique=True, blank=False, null=False)
    selector_type = models.ForeignKey(VariantSelectorType, on_delete=models.CASCADE)
    value = models.CharField(max_length=256, unique=True, blank=False, null=False)
    extra_info = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.selector_type} - {self.value} - {self.digikala_id}'


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    dkpc = models.IntegerField(unique=True, blank=False, null=False)
    price_min = models.IntegerField(blank=False, null=False)
    stop_loss = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True, blank=False, null=False)
    has_competition = models.BooleanField(default=True, blank=False, null=False, editable=False)
    selector = models.ForeignKey(
        VariantSelector,
        on_delete=models.PROTECT,
        related_name='variants',
    )

    actual_product = models.ForeignKey(
        'ActualProduct',
        on_delete=models.PROTECT,
        related_name='variants',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'selector'],
                name='unique_product_selector'
            )
        ]

    def __str__(self):
        return f'{self.dkpc}'


__all__ = [
    'Brand',
    'ActualProduct',
    'Product',
    'ProductType',
    'VariantSelectorType',
    'VariantSelector',
    'ProductVariant',
]
