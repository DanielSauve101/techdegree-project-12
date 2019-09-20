from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """Defines a model manager for User model with no username field."""

    def create_user(self, email, password):
        if not email:
            raise ValueError("Email is required.")
        email = self.normalize_email(email)
        user = self.model(
            email=email
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    
class User(AbstractUser):
    """New User model."""
    username = None
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    