from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserRegistrationView,
    login_user,
    login_page,
    user_home,
    logout_user,
    TransactionViewSet,
    CategoryViewSet,
    MonthlyBudgetViewSet,
)
from . import views

router = DefaultRouter()
router.register(r"transactions", TransactionViewSet, basename="transaction")
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"budgets", MonthlyBudgetViewSet, basename="budget")

urlpatterns = [
    # API routes
    path("api/register/", UserRegistrationView.as_view(), name="api_register"),
    path("api/login/", login_user, name="api_login"),
    path("api/", include(router.urls)),

    # Template routes
    path("login/", login_page, name="login_page"),
    path("home/", user_home, name="user_home"),
    path("logout/", logout_user, name="logout_user"),
    path("add-transaction/", views.add_transaction, name="add_transaction"),
    path("add-category/", views.add_category, name="add_category"),
    path("add-budget/", views.add_budget, name="add_budget"),
]
