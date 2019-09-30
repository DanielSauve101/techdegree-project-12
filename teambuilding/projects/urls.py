from django.urls import path

from .views import CreateProjectView, DetailProjectView


app_name = 'projects'
urlpatterns = [
    path('project/create/', CreateProjectView.as_view(), name='project-create'),
    path('project/detail/<slug:slug>/', DetailProjectView.as_view(), name='project-detail'),
]
