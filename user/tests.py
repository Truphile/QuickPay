from django.test import TestCase
from django.urls import reverse


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
                "email": "chiedoziegochiamaka@gmail.com",
                "password": "helix456"
            }