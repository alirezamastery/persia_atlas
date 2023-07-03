from django.core.management import BaseCommand
from django.db.models import Prefetch

from shop.models import *
from shop.serializers import *


class Command(BaseCommand):

    def handle(self, *args, **options):
        instance = ProductCategory.objects.last()
        attributes = ProductCategoryAttribute.objects \
            .filter(category=instance) \
            .select_related('attribute').values_list('attribute')
        print(attributes)
