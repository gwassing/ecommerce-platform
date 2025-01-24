from django.db import models
from accounts.models import UserProfile
from products.models import Product


class Cart(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f"{self.user_profile.user.username}'s cart"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.product.item_name


