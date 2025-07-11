from django.contrib import admin
from accounts import models

admin.site.register(models.User)
admin.site.register(models.ShippingDetails)
admin.site.register(models.Order)
