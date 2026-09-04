from django.contrib.auth.models import AbstractUser
from django.db import models


# to extend the User model i create a new model that extends AbstractUser
class User(AbstractUser):
    email = models.EmailField(unique=True)


