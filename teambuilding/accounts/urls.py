from django.contrib.auth import views as auth_views
from django.urls import path


from .views import CreateProfileView, LogInView, LogOutView, SignUp

app_name = 'accounts'
urlpatterns = [
    path('signup/', SignUp.as_view(), name="signup"),
    path('login/', LogInView.as_view(), name="login"),
    path('logout/', LogOutView.as_view(), name="logout"),
    path('profile/form/', CreateProfileView.as_view(), name="profile-form"),
]
