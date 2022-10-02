from pprint import pprint
from django.forms import ModelForm, ValidationError
from .models import ProductVariant, Product, ActualProduct


class ProductVariantAdminForm(ModelForm):
    class Meta:
        model = ProductVariant
        fields = '__all__'

    def clean(self):
        super().clean()
        product = self.cleaned_data.get('product')
        if product:
            dkpc = self.cleaned_data.get('dkpc')
            print(self.cleaned_data)
            variants = product.variants.exclude(dkpc=dkpc).all()
            # selector_values = self.cleaned_data.get('selector_values')
            # if len(selector_values) > 1:
            #     msg = f'you can not select more than one selector value'
            #     raise ValidationError(msg)
            # already_exists = []
            # for var in variants:
            #     for value in selector_values:
            #         if value in var.selector_values.all():
            #             already_exists.append(value)
            # if product.variants.filter(selector_values__in=selector_values).exists():
            #     values = ' | '.join([s.value for s in selector_values])
            #     msg = f'Variant for " {product.title} " with selectors: {values} already exists'
            #     raise ValidationError(msg)
            # if len(already_exists) > 0:
            #     values = ' | '.join([s.value for s in already_exists])
            #     msg = f'Variant for " {product.title} " with selectors: {values} already exists'
            #     raise ValidationError(msg)
        return self.cleaned_data


class ActualProductAdminForm(ModelForm):
    class Meta:
        model = ActualProduct
        fields = '__all__'

    def clean(self):
        super().clean()
        variants = self.cleaned_data.get('variants')
        print(variants)
        return self.cleaned_data
