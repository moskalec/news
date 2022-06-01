from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)


class BaseModel(models.Model):
    created = models.DateTimeField(
        auto_now_add=True
    )

    updated = models.DateTimeField(
        auto_now=True
    )

    active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        verbose_name = _('%(class)')
        verbose_name_plural = _('%(class)s')
