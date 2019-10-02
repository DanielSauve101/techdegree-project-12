from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from projects.models import Position


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


class Profile(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name="profile"
        )
    slug = models.SlugField(allow_unicode=True, unique=True)
    name = models.CharField(max_length=60)
    description = models.TextField()
    profile_picture = models.ImageField(
        upload_to="profile_picture", 
        default='profile_picture/default_pic.jpg'
        )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        email = self.user.email.split("@", 1)
        self.slug = slugify(email[0])
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("accounts:profile-detail", kwargs={"slug": self.slug})


class Skill(models.Model):
    profile = models.ForeignKey(
        Profile, 
        on_delete=models.CASCADE,
        related_name="skill"
        )
    skills = models.CharField(
        max_length=3,
        choices=Position.POSITION_CHOICES
        )

    def __str__(self):
        return self.get_skills_display()


class MyProject(models.Model):
    profile = models.ForeignKey(
        Profile, 
        on_delete=models.CASCADE,
        related_name="myproject"
        )
    title = models.CharField(max_length=60, blank=True)
    url = models.URLField(blank=True)

    def __str__(self):
        return self.title
