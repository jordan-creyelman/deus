from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Utilisateur de l'application DEUS ARCHIVE."""

    email = models.EmailField("adresse e-mail", unique=True)

    def __str__(self):
        return self.username
