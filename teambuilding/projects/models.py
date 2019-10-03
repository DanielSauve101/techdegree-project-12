from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Project(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(allow_unicode=True)
    project_owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name="project"
        )
    description = models.TextField()
    timeline = models.TextField()
    applicant_requirements = models.TextField(blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("projects:project-detail", kwargs={"slug": self.slug})
    

class Position(models.Model):
    ANDROID_DEVELOPER = 'AND'
    DESIGNER = 'DES'
    IOS_DEVELOPER = 'IOS'
    JAVA_DEVELOPER = 'JAV'
    PHP_DEVELOPER = 'PHP'
    PYTHON_DEVELOPER = 'PYT'
    RAILS_DEVELOPER = 'RAI'
    WORDPRESS_DEVELOPER = 'WOR'
    OTHER = 'OTH'

    POSITION_CHOICES = [
    (ANDROID_DEVELOPER, 'Android Developer'),
    (DESIGNER, 'Designer'),
    (IOS_DEVELOPER, 'IOS Developer'),
    (JAVA_DEVELOPER, 'Java Developer'),
    (PHP_DEVELOPER, 'PHP Developer'),
    (PYTHON_DEVELOPER, 'Python Developer'),
    (RAILS_DEVELOPER, 'Rails Developer'),
    (WORDPRESS_DEVELOPER, 'Wordpress Developer'),
    (OTHER, 'Other')
    ]

    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE,
        related_name="position"
        )
    title = models.CharField(
        max_length=3,
        choices=POSITION_CHOICES,
        )
    description = models.TextField(blank=True)
    position_filled = models.BooleanField(default=False)

    def __str__(self):
        return self.get_title_display()


