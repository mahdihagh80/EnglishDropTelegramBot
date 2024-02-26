from django.contrib import admin
from .models import Package, Transaction, TelegramUser, TelegramChannel, InstagramPage, BankAccount


@admin.register(TelegramUser) 
class TelegramUserAdmin(admin.ModelAdmin):
    search_fields = ['full_name']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    search_fields = ['user__full_name']
    list_filter = ['state', 'links_sent']

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ['links_sent']
        return []


admin.site.register(Package)
admin.site.register(TelegramChannel)
admin.site.register(InstagramPage)
admin.site.register(BankAccount)