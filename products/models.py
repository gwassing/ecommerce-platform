from django.db import models
from datetime import date


class Product (models.Model):
    category = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    item_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    date_created = models.DateField(default=date.today)

    def __str__(self):
        return self.item_name

