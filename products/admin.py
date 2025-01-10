from django.contrib import admin

from products import models


class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    extra = 0


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductImageInline
    ]
