from django.contrib import admin

from .models import (Product, ProductType, ProductTypeSelector,
                     ProductTypeSelectorValue, ProductVariant, ActualProduct,
                     Brand)
from .forms import ProductVariantAdminForm, ActualProductAdminForm


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'dkp', 'is_active', 'type', 'pk')
    list_filter = ('is_active',)
    search_fields = ('title', 'dkp')

    def has_delete_permission(self, request, obj=None):
        if request.user.mobile == '09358578419':
            return True
        return False

    def get_readonly_fields(self, request, obj=None):
        if request.user.mobile == '09358578419':
            return []
        else:
            return ['title', 'dkp', 'type']


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant


class ActualProductAdmin(admin.ModelAdmin):
    # inlines = [ProductVariantInline]
    pass


class ProductVariantAdmin(admin.ModelAdmin):
    form = ProductVariantAdminForm
    list_display = ('dkpc', 'product', 'get_selectors', 'price_min', 'is_active', 'no_competition')
    list_editable = ('price_min',)
    readonly_fields = ('is_active',)
    search_fields = ('dkpc', 'product__title', 'selector_values__value')
    list_filter = ('is_active',)
    save_on_top = True
    filter_horizontal = ['selector_values']

    @admin.display(description='selectors')
    def get_selectors(self, obj):
        return ' | '.join([f'{s.value} - {s.digikala_id}' for s in obj.selector_values.all()])

    def no_competition(self, obj):
        return not obj.has_competition

    no_competition.boolean = True

    def has_delete_permission(self, request, obj=None):
        if request.user.mobile == '09358578419':
            return True
        return False

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return []
        if request.user.mobile == '09358578419':
            return []
        else:
            return ['product', 'dkpc', 'selector_values']

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        print(fields)
        # ff = IntegerField()
        # fields.append('no_competition')
        return fields


class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_selectors')

    @admin.display(description='selectors')
    def get_selectors(self, obj):
        return ' | '.join([f'{s.title}' for s in obj.selectors.all()])


class ProductTypeSelectorValueAdmin(admin.ModelAdmin):
    list_display = ('digikala_id', 'value', 'selector')
    readonly_fields = ('digikala_id', 'value', 'selector')


admin.site.register(Product, ProductAdmin)
admin.site.register(Brand)
admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(ProductTypeSelector)
admin.site.register(ProductTypeSelectorValue, ProductTypeSelectorValueAdmin)
admin.site.register(ProductVariant, ProductVariantAdmin)
admin.site.register(ActualProduct, ActualProductAdmin)
