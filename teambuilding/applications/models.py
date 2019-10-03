from django.conf import settings
from django.db import models

from projects.models import Position, Project 


class Applicant(models.Model):
    NEW = 'NEW'
    ACCEPTED = 'ACC'
    REJECTED = 'REJ'
    
    APPLICANT_CHOICES = [
    (NEW, 'New Applicants'),
    (ACCEPTED, 'Accepted'),
    (REJECTED, 'Rejected'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="applicant"
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="applicant_project"
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        related_name="applicant_position"
    )
    status = models.CharField(
        max_length=3,
        choices=APPLICANT_CHOICES,
        default=NEW
    )

    def __str__(self):
        return "{} for {} project".format(self.user.profile.name, self.project)
