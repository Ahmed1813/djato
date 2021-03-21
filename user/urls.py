from django.urls import path
from .views import (
    UserRegistraionView,
    UserLoginView,
    logout_view,
)

app_name = "user"
urlpatterns = [
    path("register/", UserRegistraionView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
]
