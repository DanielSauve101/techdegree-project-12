from django.contrib.auth import views as auth_views
from django.urls import path


from .views import CreateProfileView, DetailProfileView, LogInView, LogOutView, SignUp, UpdateProfileView

app_name = 'accounts'
urlpatterns = [
    path('signup/', SignUp.as_view(), name="signup"),
    path('login/', LogInView.as_view(), name="login"),
    path('logout/', LogOutView.as_view(), name="logout"),
    path('profile/form/', CreateProfileView.as_view(), name="profile-form"),
    path('profile/detail/<slug:slug>/', DetailProfileView.as_view(), name="profile-detail"),
    path('profile/update/<slug:slug>/', UpdateProfileView.as_view(), name="profile-update"),
]
