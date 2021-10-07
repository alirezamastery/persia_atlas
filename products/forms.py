from pprint import pprint
from django.forms import ModelForm, ValidationError
from .models import ProductVariant, Product


class ProductVariantAdminForm(ModelForm):
    class Meta:
        model = ProductVariant
        fields = '__all__'

    def clean(self):
        super().clean()
        product = self.cleaned_data.get('product')
        selector_values = self.cleaned_data.get('selector_values')
        already_exists = []
        variants = product.variants.all()
        for var in variants:
            for value in selector_values:
                if value in var.selector_values.all():
                    already_exists.append(value)
        # if product.variants.filter(selector_values__in=selector_values).exists():
        #     values = ' | '.join([s.value for s in selector_values])
        #     msg = f'Variant for " {product.title} " with selectors: {values} already exists'
        #     raise ValidationError(msg)
        if len(already_exists) > 0:
            values = ' | '.join([s.value for s in already_exists])
            msg = f'Variant for " {product.title} " with selectors: {values} already exists'
            raise ValidationError(msg)
        return self.cleaned_data
