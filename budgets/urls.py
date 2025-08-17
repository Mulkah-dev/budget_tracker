# budget_tracker/urls.py  (or your app's urls.py)
from django.urls import path, include
from . import views
from .views import register_user

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('api/', include('users.urls')),
]
