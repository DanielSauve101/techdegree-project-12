from django.urls import path

from .views import CreateApplicantView, CreateProjectView, DeleteProjectView, DetailProjectView, ListApplicationsView, UpdateProjectView


app_name = 'projects'
urlpatterns = [
    path('project/create/', CreateProjectView.as_view(), name='project-create'),
    path('project/detail/<slug:slug>/', DetailProjectView.as_view(), name='project-detail'),
    path('project/update/<slug:slug>/', UpdateProjectView.as_view(), name='project-update'),
    path('project/delete/<slug:slug>/', DeleteProjectView.as_view(), name='project-delete'),
    path('project/apply/<slug:slug>/<int:pk>/', CreateApplicantView.as_view(), name='applicant-create'),
    path('applications/', ListApplicationsView.as_view(), name="applications-list"),
]
