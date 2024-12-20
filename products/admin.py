from django.contrib import admin

from products import models


class ProductImageInline(admin.TabularInline):
    model = models.ProductImage


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    pass
    inlines = [
        ProductImageInline
        ]
