from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from categories.models import Category
from budgets.models import Transaction

User = get_user_model()

class ReportTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        url = reverse("token_obtain_pair")
        response = self.client.post(url, {"username": "testuser", "password": "testpass123"}, format="json")
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.category_income = Category.objects.create(name="Salary", user=self.user)
        self.category_expense = Category.objects.create(name="Food", user=self.user)

        Transaction.objects.create(user=self.user, category=self.category_income, amount=100000, type="income", transaction_date="2025-08-20")
        Transaction.objects.create(user=self.user, category=self.category_expense, amount=5000, type="expense", transaction_date="2025-08-20")

    def test_summary_report(self):
        url = reverse("transaction-summary")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_income"], 100000)
        self.assertEqual(response.data["total_expenses"], 5000)
        self.assertEqual(response.data["balance"], 95000)
