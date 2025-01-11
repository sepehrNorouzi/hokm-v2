from django.contrib import admin

from shop.models import Currency

# Register your models here.
@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    pass
