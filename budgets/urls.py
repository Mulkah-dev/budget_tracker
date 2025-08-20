# budget_tracker/urls.py  (or your app's urls.py)
from django.urls import path, include
#from . import views
from rest_framework.routers import DefaultRouter
from .views import TransactionViewSet, register_user, login_user

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transaction')
urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('api/', include('users.urls')),
    path('', include(router.urls)),
]
