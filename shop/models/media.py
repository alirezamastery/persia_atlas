from django.db import models


__all__ = [
    'ProductImage',
]


class ProductImage(models.Model):
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE, related_name='images')
    file = models.ImageField('products/img')
    is_main = models.BooleanField(default=False)
    description = models.TextField(default='', blank=True)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_main:
            other_images = ProductImage.objects.filter(product=self.product).exclude(id=self.id)
            for img in other_images:
                img.is_main = False
            ProductImage.objects.bulk_update(other_images, ['is_main'])
