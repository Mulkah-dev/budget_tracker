from django.urls import path
from .views import test_view, UserRegisterView, CustomAuthToken, LogoutView

urlpatterns = [
    path("test/", test_view, name="test"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", CustomAuthToken.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
