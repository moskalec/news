from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class User(AbstractUser):
    email = models.EmailField(unique=True)

    def get_absolute_url(self):
        return reverse('account:user_detail', kwargs={'slug': self.username})


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
