from django.urls import path
from .views import transaction_summary

urlpatterns = [
    path("summary/", transaction_summary, name="transaction-summary"),
]
