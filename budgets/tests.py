from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from categories.models import Category

User = get_user_model()

class TransactionTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        url = reverse("token_obtain_pair")
        response = self.client.post(url, {"username": "testuser", "password": "testpass123"}, format="json")
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.category = Category.objects.create(name="Food", user=self.user)

    def test_create_transaction(self):
        url = reverse("transaction-list")
        data = {
            "amount": "5000.00",
            "transaction_date": "2025-08-20",
            "type": "expense",
            "category": self.category.id,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_transaction_list(self):
        url = reverse("transaction-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_category_rejected(self):
        url = reverse("transaction-list")
        data = {
            "amount": "1000.00",
            "transaction_date": "2025-08-20",
            "type": "expense",
            "category": 9999,  # invalid pk
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
