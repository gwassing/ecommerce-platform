from django.db import models


class Product (models.Model):
    category = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    date_published = models.DateField(auto_now_add=True)

