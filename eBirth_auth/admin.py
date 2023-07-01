from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from eBirth_auth.models import User


class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'cert_no', 'pic', 'is_hospital', 'is_hospital_admin', 'is_staff',
                    'is_superuser', 'date_joined', 'last_login', 'is_active')
    # You can search by both email and cert_no
    search_fields = ('email', 'cert_no')
    ordering = ()
    readonly_fields = ('date_joined', 'last_login',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('cert_no', 'pic')}),
        ('Permissions', {'fields': (
            'is_hospital', 'is_hospital_admin', 'is_staff', 'is_superuser', 'is_active')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'cert_no', 'password1', 'password2'),
        }),
    )

# Register your models here.
admin.site.register(User, UserAdmin)
