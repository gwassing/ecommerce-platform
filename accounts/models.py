from django.db import models
from django.contrib.auth.models import AbstractUser

from cart.models import Cart
from products.models import Product


class User(AbstractUser):
    location = models.CharField(max_length=50, blank=True, null=True)


class ShippingDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    address = models.CharField(max_length=200)
    postcode = models.CharField(max_length=5)
    city = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.last_name}, {self.address}, {self.city}'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_details = models.ForeignKey(ShippingDetails, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        created_formatted = self.created.strftime("%Y-%m-%d %H:%M")

        return f"{self.user} - {self.purchased_items.count()} items - {created_formatted}"


class PurchasedItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='purchased_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product}, {self.quantity}"
