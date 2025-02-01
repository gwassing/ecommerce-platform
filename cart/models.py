from django.conf import settings
from django.db import models
from products.models import Product


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f"{self.user}'s cart"

    def get_total_price(self):
        total_price = 0
        for item in self.cart_items.all():
            total_price += item.product.price
        return total_price


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=False, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.product.item_name


