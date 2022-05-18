from django.db import models


class BaseModel(models.Model):
    created = models.DateTimeField(
        auto_now_add=True
    )

    updated = models.DateTimeField(
        null=True,
        blank=True
    )

    active = models.BooleanField(default=True)

    class Meta:
        abstract = True