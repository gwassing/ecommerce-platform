from django.contrib import admin
from cart import models


class CartItem(admin.TabularInline):
    model = models.CartItem
    extra = 0


@admin.register(models.Cart)
class Cart(admin.ModelAdmin):
    inlines = [
        CartItem
    ]
