from django.core.validators import MinValueValidator
from django.db import models
from datetime import date
from django.contrib.postgres.fields import ArrayField


from django.db.models import CheckConstraint, Q
from django.dispatch import receiver
from django.db.models.signals import pre_delete

PRODUCT_CATEGORIES = {
    "SHOES": "Shoes",
    "CLOTHING": "Clothing",
    "ACCESSORIES": "Accessories"
}


class Product (models.Model):
    category = models.CharField(max_length=50, choices=PRODUCT_CATEGORIES)
    brand = models.CharField(max_length=50)
    item_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.0)])
    date_created = models.DateField(default=date.today)
    colors = ArrayField(models.CharField(max_length=100), null=True, blank=True, default=list)

    def __str__(self):
        return self.item_name

    class Meta:
        constraints = [
            CheckConstraint(check=Q(price__gte=0.01), name='positive_price')
        ]


class ProductImage(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="images/")


@receiver(pre_delete, sender=ProductImage)
def delete_s3_image(sender, instance, **kwargs):
    # delete image on s3 when product image is deleted
    print(f"deleted: {instance.image.name}")
    instance.image.delete()
