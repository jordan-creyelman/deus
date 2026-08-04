from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class UserModelTests(TestCase):
    def test_create_user(self):
        user = get_user_model().objects.create_user(
            username="alice",
            email="alice@example.com",
            password="mot-de-passe-solide",
        )

        self.assertEqual(str(user), "alice")
        self.assertEqual(user.email, "alice@example.com")
        self.assertTrue(user.check_password("mot-de-passe-solide"))

    def test_email_must_be_unique(self):
        user_model = get_user_model()
        user_model.objects.create_user(
            username="alice",
            email="joueur@example.com",
            password="mot-de-passe-solide",
        )

        with self.assertRaises(IntegrityError), transaction.atomic():
            user_model.objects.create_user(
                username="bob",
                email="joueur@example.com",
                password="autre-mot-de-passe",
            )


class RegisterApiTests(APITestCase):
    def setUp(self):
        self.url = reverse("register")
        self.payload = {
            "username": "nouveau_joueur",
            "email": "joueur@example.com",
            "password": "Archive!2026Solide",
            "password_confirm": "Archive!2026Solide",
        }

    def test_register_user(self):
        response = self.client.post(self.url, self.payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn("password", response.data)
        user = get_user_model().objects.get(username="nouveau_joueur")
        self.assertTrue(user.check_password("Archive!2026Solide"))

    def test_reject_different_passwords(self):
        self.payload["password_confirm"] = "UnAutreMotDePasse!2026"

        response = self.client.post(self.url, self.payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password_confirm", response.data)
        self.assertFalse(get_user_model().objects.exists())

    def test_reject_duplicate_email(self):
        get_user_model().objects.create_user(
            username="joueur_existant",
            email=self.payload["email"],
            password="Archive!2026Solide",
        )

        response = self.client.post(self.url, self.payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)


class JwtAuthenticationTests(APITestCase):
    def setUp(self):
        self.password = "Archive!2026Solide"
        self.user = get_user_model().objects.create_user(
            username="alice",
            email="alice@example.com",
            password=self.password,
        )

    def test_obtain_and_refresh_tokens_in_httponly_cookies(self):
        login_response = self.client.post(
            reverse("token-obtain-pair"),
            {"username": self.user.username, "password": self.password},
            format="json",
        )

        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertNotIn("access", login_response.data)
        self.assertNotIn("refresh", login_response.data)
        self.assertTrue(login_response.cookies["deus_access"]["httponly"])
        self.assertTrue(login_response.cookies["deus_refresh"]["httponly"])
        refresh_response = self.client.post(reverse("token-refresh"), format="json")
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn("deus_access", refresh_response.cookies)
        self.assertTrue(refresh_response.cookies["deus_access"].value)

    def test_access_protected_route_with_token(self):
        login_response = self.client.post(
            reverse("token-obtain-pair"),
            {"username": self.user.username, "password": self.password},
            format="json",
        )

        response = self.client.get(reverse("current-user"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "alice")

    def test_reject_protected_route_without_token(self):
        response = self.client.get(reverse("current-user"))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_deletes_and_blacklists_tokens(self):
        self.client.post(
            reverse("token-obtain-pair"),
            {"username": self.user.username, "password": self.password},
            format="json",
        )
        refresh = self.client.cookies["deus_refresh"].value

        response = self.client.post(reverse("logout"), format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.cookies["deus_access"]["max-age"], 0)
        self.assertEqual(response.cookies["deus_refresh"]["max-age"], 0)

        self.client.cookies["deus_refresh"] = refresh
        refresh_response = self.client.post(reverse("token-refresh"), format="json")
        self.assertEqual(refresh_response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_reject_invalid_password(self):
        response = self.client.post(
            reverse("token-obtain-pair"),
            {"username": self.user.username, "password": "incorrect"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_registration_remains_public(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "bob",
                "email": "bob@example.com",
                "password": "Archive!2026Solide",
                "password_confirm": "Archive!2026Solide",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
