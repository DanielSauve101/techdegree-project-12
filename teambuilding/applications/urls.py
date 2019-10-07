from django.urls import path

from .views import ListApplicationsView

app_name = 'applications'
urlpatterns = [
    path('', ListApplicationsView.as_view(), name="applications-list"),
]
