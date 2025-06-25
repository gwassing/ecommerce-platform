from django.conf import settings
from django.db import models

from products.models import Product


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f"{self.user}'s cart"

    def get_items(self):
        return self.cart_items.all().select_related('product')

    def get_total_price(self):
        return sum((item.product.price * item.quantity) for item in self.get_items())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=False, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)
    quantity = models.PositiveIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.item_name

    class Meta:
        ordering = ["-created"]


