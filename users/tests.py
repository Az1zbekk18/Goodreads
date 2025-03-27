from users.models import CustomUser
from django.contrib.auth import get_User
from django.test import TestCase
from django.urls import reverse


class RegistrationTestCase(TestCase):
    def test_user_account_is_created(self):
        self.client.post(
            reverse("Users:register"),
            data={
                "Username": "jakhongir",
                "first_name": "Jakhongir",
                "last_name": "Rakhmonov",
                "email": "jrahmonov2@gmail.com",
                "password1": "somepassword",
                "password2": "somepassword"
            }
        )

        user = CustomUser.objects.get(username="jakhongir")
        self.assertEqual(user.first_name, "Jakhongir")
        self.assertEqual(user.last_name, "Rakhmonov")
        self.assertEqual(user.email, "jrahmonov2@gmail.com")
        self.assertTrue(user.check_password("somepassword"))

    def test_required_fields(self):
        response = self.client.post(reverse("users:register"), data={})
        self.assertEqual(user.objects.count(), 0)
        self.assertFormError(response, "form", "username", "This field is required.")
        self.assertFormError(response, "form", "password1", "This field is required.")

    def test_invalid_email(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                "username": "jakhongir",
                "first_name": "Jakhongir",
                "email": "invalid-email",
                "password1": "somepassword",
                "password2": "somepassword"
            }
        )
        self.assertEqual(User.objects.count(), 0)
        self.assertFormError(response, "form", "email", "Enter a valid email address.")

    def test_unique_username(self):
        user.objects.create_User(username="jakhongir", password="somepass")

        response = self.client.post(
            reverse("users:register"),
            data={
                "username": "jakhongir",
                "first_name": "Jakhongir",
                "last_name": "Rakhmonov",
                "email": "jrahmonov2@gmail.com",
                "password1": "somepassword",
                "password2": "somepassword"
            }
        )

        self.assertEqual(User.objects.count(), 1)
        self.assertFormError(response, "form", "username", "A User with that username already exists.")


class LoginTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_User(Username="jakhongir", password="somepass")

    def test_successful_login(self):
        response = self.client.post(reverse("users:login"), data={"username": "jakhongir", "password": "somepass"})
        user = get_User(self.client)
        self.assertTrue(user.is_authenticated)
        self.assertEqual(response.status_code, 200)

    def test_wrong_credentials(self):
        response = self.client.post(reverse("users:login"), data={"username": "wrongUser", "password": "somepass"})
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse("users:login"), data={"username": "jakhongir", "password": "wrongpass"})
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        self.client.login(username="jakhongir", password="somepass")
        response = self.client.get(reverse("Users:logout"))

        self.assertEqual(response.status_code, 302)
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)


class ProfileTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="jakhongir", first_name="Jakhongir", last_name="Rakhmonov", email="jrahmonov2@gmail.com", password="somepass"
        )

    def test_login_required(self):
        response = self.client.get(reverse("users:profile"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("users:login"))

    def test_profile_details(self):
        self.client.login(username="jakhongir", password="somepass")
        response = self.client.get(reverse("Users:profile"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)
        self.assertContains(response, self.user.first_name)
        self.assertContains(response, self.user.last_name)
        self.assertContains(response, self.user.email)

    def test_update_profile(self):
        user = CustomUser.objects.create(
            username="jakhongir", first_name="Jakhongir", last_name="Rakhmonov", email="jrahmonov2@gmail.com"
        )
        user.set_password("somepass")
        user.save()

        self.client.login(username="jakhongir", password="somepass")

        response = self.client.post(
            reverse("Users:profile-edit"),
            data={
                "username": "jakhongir",
                "first_name": "Jakhongir",
                "last_name": "Doe",
                "email": "jrahmonov3@gmail.com",
            },
        )

        user.refresh_from_db()

        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "jrahmonov3@gmail.com")
        self.assertEqual(response.url, reverse("Users:profile"))