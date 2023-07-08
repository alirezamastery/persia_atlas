from django.db import models


__all__ = [
    'ProductVariant',
    'VariantSelectorType',
    'VariantSelectorValue',
]


class ProductVariant(models.Model):
    product = models.ForeignKey(
        'shop.Product',
        on_delete=models.CASCADE,
        related_name='variants'
    )
    selector_value = models.ForeignKey(
        'shop.VariantSelectorValue',
        on_delete=models.PROTECT,
        related_name='product_variants'
    )

    is_active = models.BooleanField(default=True)
    price = models.PositiveBigIntegerField()
    inventory = models.PositiveIntegerField()
    max_in_order = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'selector_value'],
                name='unique_product_selector_value'
            )
        ]

    def __str__(self):
        return f'{self.product} - {self.selector_value.value}'


class VariantSelectorType(models.Model):
    class CodeChoices(models.TextChoices):
        SIZE = 'SIZE'
        COLOR = 'COLOR'

    title = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=255, unique=True, choices=CodeChoices.choices)

    def __str__(self):
        return f'{self.title}'


class VariantSelectorValue(models.Model):
    type = models.ForeignKey(
        'shop.VariantSelectorType',
        on_delete=models.PROTECT,
        related_name='values'
    )
    title = models.CharField(max_length=255, unique=True)
    value = models.CharField(max_length=255, unique=True)
    extra_info = models.TextField(default='')

    def __str__(self):
        return f'{self.type} - {self.value}'
