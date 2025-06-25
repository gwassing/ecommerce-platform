from django.db import models


class Status(models.TextChoices):
    ARCHIVED = "archived", "Archived"
    ACTIVE = "active", "Active"


class StatusMixin(models.Model):
    status = models.CharField(max_length=20, choices=Status, default=Status.ACTIVE)

    class Meta:
        abstract = True
