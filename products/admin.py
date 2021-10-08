from django.contrib import admin

from .models import Product, ProductType, ProductTypeSelector, ProductTypeSelectorValue, ProductVariant
from .forms import ProductVariantAdminForm


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'dkp', 'is_active', 'type', 'pk')


class ProductVariantAdmin(admin.ModelAdmin):
    form = ProductVariantAdminForm
    list_display = ('dkpc', 'product', 'get_selectors', 'price_min', 'is_active', 'no_competition')
    list_editable = ('price_min', 'is_active')
    search_fields = ('dkpc', 'product__title', 'selector_values__value')
    list_filter = ('is_active',)

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


class ProductTypeSelectorValueAdmin(admin.ModelAdmin):
    list_display = ('digikala_id', 'value', 'selector', 'pk')
    readonly_fields = ('digikala_id', 'value', 'selector')


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductType)
admin.site.register(ProductTypeSelector)
admin.site.register(ProductTypeSelectorValue, ProductTypeSelectorValueAdmin)
admin.site.register(ProductVariant, ProductVariantAdmin)
