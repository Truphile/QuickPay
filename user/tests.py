from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from user.models import User


# Create your tests here.
class TestSignup(TestCase):
    # def test_signup_returns_201(self):
    #     url = reverse("register")
    #     data={
    #             "username": "nissiz",
    #             "email": "angelonissil@gmail.com",
    #             "password": "StrongPassword123!",
    #             "first_name": "Nissil",
    #             "last_name": "Sam",
    #             "phone": "08012347178"
    #     }
    #
    #     response = self.client.post(url, data)
    #     self.ass

        def setUp(self):
            self.url = reverse("register")
            self.login_url = reverse("login")
            self.data = {
                "first_name": "Achalugo",
                "last_name": "Chiamie",
                "email": "chiedoziegochiamaka@gmail.com",
                "phone": "08101235568",
                "username": "Chimasky",
                "password": "helix456",
            }
            self.login_data = {
                "email": "angelonissil@gmail.com",
                "password": "hello123@"
            }


        def test_signup_returns_201(self):
            response = self.client.post(self.url, self.data, format="json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(User.objects.count(), 1)