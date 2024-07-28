# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Wallet, Notification

class WalletInline(admin.StackedInline):
    model = Wallet
    can_delete = False
    verbose_name_plural = 'wallet'

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'phone_number', 'is_active', 'is_premium', 'transaction_pin')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'transaction_pin')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_premium', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone_number', 'password1', 'password2'),
        }),
    )
    inlines = (WalletInline,)
    search_fields = ('username', 'email', 'phone_number')
    ordering = ('username',)


class WalletAdmin(admin.ModelAdmin):
    model = Wallet
    list_display = ('wallet_name', 'balance', 'last_funded')


class NotificationAdmin(admin.ModelAdmin):
    model = Notification
    list_display = ('user', 'date_sent', 'is_read')

admin.site.register(Notification, NotificationAdmin)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Wallet, WalletAdmin)
