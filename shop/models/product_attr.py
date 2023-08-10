from django.db import models


__all__ = [
    'Attribute',
]


class Attribute(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(default='', blank=True)

    def __str__(self):
        return self.title

