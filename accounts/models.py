from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    Attributes:
        role (str): Either 'user' (default) or 'admin'.
        email (str): Unique email address used for authentication.
        """
    class Role(models.TextChoices):
        USER = 'user', 'User'
        ADMIN = 'admin', 'Admin'

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.USER)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def is_admin(self):
        """Return True if this user has the admin role."""
        return self.role == self.Role.ADMIN
    
    def __str__(self):
        return self.email
    