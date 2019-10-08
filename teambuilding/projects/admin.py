from django.contrib import admin

from .models import Applicant, Project, Position


admin.site.register(Project)
admin.site.register(Position)
admin.site.register(Applicant)