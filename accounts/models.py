from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.db import models

from django_countries.fields import CountryField

from churches.models import Church


class User(AbstractUser):
    country = CountryField()

    member = models.ManyToManyField(Church, related_name='members')
    membership_validated = models.BooleanField(default=False)
