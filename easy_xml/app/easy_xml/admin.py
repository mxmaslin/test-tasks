from django.contrib import admin

from easy_xml.models import Product, Tariff, Promotion


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    pass


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    pass
