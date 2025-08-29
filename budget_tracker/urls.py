# budget_tracker/urls.py (project root)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("budgets.urls")),  # include your app’s urls
]
