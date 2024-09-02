from django.db import models
from datetime import date

from django.db.models import CheckConstraint, Q

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

    class Meta:
        constraints = [
            CheckConstraint(check=Q(price__gte=0.01), name='positive_price')
        ]

