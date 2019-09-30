from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Project(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(allow_unicode=True)
    project_owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
        )
    description = models.TextField()
    timeline = models.TextField()
    applicant_requirements = models.TextField()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("projects:project-detail", kwargs={"slug": self.slug})
    

class Position(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=60)
    description = models.TextField()
    position_filled = models.BooleanField(default=False)

    def __str__(self):
        return self.title


