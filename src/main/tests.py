from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class HomeViewTests(TestCase):
    def test_home_renders_existing_template_for_authenticated_user(self):
        user = User.objects.create_user(username="tester", password="secret123")
        self.client.force_login(user)

        response = self.client.get(reverse("main:home"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "base/home.html")
