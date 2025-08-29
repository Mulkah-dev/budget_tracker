from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationTests(APITestCase):
    def test_user_can_register(self):
        url = reverse("register")
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123"
        }
        response = self.client.post(url, data, format="json")
        print("REGISTER RESPONSE:", response.data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, "test@example.com")


class UserLoginTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="loginuser",
            email="login@example.com",
            password="loginpass123"
        )

    def test_user_can_login(self):
        url = reverse("login")
        data = {
            "username": "loginuser",
            "password": "loginpass123"
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # ✅ Adjusted checks to match TokenAuth response
        self.assertIn("token", response.data)
        self.assertEqual(response.data["email"], "login@example.com")
        self.assertEqual(response.data["user_id"], self.user.id)
