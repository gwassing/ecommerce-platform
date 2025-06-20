from django.db import models


STATUSES = {
    "ARCHIVED": "Archived",
    "ACTIVE": "Active"
}


class StatusMixin(models.Model):
    status = models.CharField(max_length=20, choices=STATUSES)

    class Meta:
        abstract = True
