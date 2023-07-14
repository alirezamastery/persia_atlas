from django.db import models
from utils.slug import unique_slugify


__all__ = [
    'Brand',
    'Product',
    'ProductAttributeValue',
]


class Brand(models.Model):
    title = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.title}'


class Product(models.Model):
    brand = models.ForeignKey(
        'shop.Brand',
        on_delete=models.PROTECT,
        related_name='products'
    )
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(default='')
    is_active = models.BooleanField(default=True, blank=True)
    slug = models.SlugField(unique=True, editable=False, blank=True)
    thumbnail = models.ImageField(upload_to='product/main_img')

    category = models.ForeignKey(
        'shop.ProductCategory',
        on_delete=models.PROTECT,
        related_name='products'
    )

    attribute_values = models.ManyToManyField(
        'shop.ProductAttribute',
        through='shop.ProductAttributeValue',
        # related_name='products', will cause error in queries!
    )

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        if self._state.adding:
            slug_str = f'{self.title}'.replace(' ', '-')
            unique_slugify(self, slug_str)
        return super().save(*args, **kwargs)


class ProductAttributeValue(models.Model):
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE)
    attribute = models.ForeignKey('shop.ProductAttribute', on_delete=models.CASCADE)

    value = models.TextField()
    extra_info = models.TextField(default='', blank=True)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'attribute'],
                name='unique_product_attribute_value'
            )
        ]
