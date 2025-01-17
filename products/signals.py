from django.dispatch import receiver
from django.db.models.signals import pre_delete

from products.models import ProductImage


@receiver(pre_delete, sender=ProductImage)
def delete_s3_image(sender, instance, **kwargs):
    # delete image on s3 when product image is deleted
    print(f"deleted: {instance.image.name}")
    instance.image.delete()
