from django.contrib import admin
from accounts import models

admin.site.register(models.User)
admin.site.register(models.ShippingDetails)
admin.site.register(models.PaymentDetails)


class PurchasedItemInline(admin.TabularInline):
    model = models.PurchasedItem
    extra = 0


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        PurchasedItemInline
    ]

