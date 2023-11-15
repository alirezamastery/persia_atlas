from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, Profile
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    ordering = ('mobile',)
    search_fields = ('mobile',)
    list_display = ('mobile', 'is_staff', 'is_active', 'pk')
    list_filter = ('is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('mobile', 'password')}),

        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),

        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide', 'extrapretty'),
            'fields':  ('mobile', 'password1', 'password2'),
        }),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)
