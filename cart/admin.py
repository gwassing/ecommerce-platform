from django.contrib import admin
from cart import models


class CartItemInline(admin.TabularInline):
    model = models.CartItem
    extra = 0


@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [
        CartItemInline
    ]
