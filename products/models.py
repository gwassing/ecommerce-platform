from django.db import models
from datetime import date

PRODUCT_CATEGORIES = {
    "SHOES": "Shoes",
    "CLOTHING": "Clothing",
    "ACCESSORIES": "Accessories"
}


class Product (models.Model):
    category = models.CharField(max_length=50, choices=PRODUCT_CATEGORIES)
    brand = models.CharField(max_length=50)
    item_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    date_created = models.DateField(default=date.today)

    def __str__(self):
        return self.item_name

