from django.urls import path

from .views import SignInView, SignOutView, SignUp

app_name = 'accounts'
urlpatterns = [
    path('signup/', SignUp.as_view(), name="signup"),
    path('signin/', SignInView.as_view(), name="signin"),
    path('signout/', SignOutView.as_view(), name="signout"),
]
