from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Character


class CharacterModelTests(TestCase):
    def setUp(self):
        self.owner = get_user_model().objects.create_user(
            username="alice",
            email="alice@example.com",
            password="mot-de-passe-solide",
        )

    def test_create_character(self):
        character = Character.objects.create(
            owner=self.owner,
            name="Akasha",
            description="Archiviste des mondes oubliés.",
        )

        self.assertEqual(str(character), "Akasha")
        self.assertEqual(character.level, 1)
        self.assertEqual(character.experience, 0)
        self.assertEqual(character.description, "Archiviste des mondes oubliés.")
        self.assertEqual(character.strength, 1)
        self.assertEqual(character.agility, 1)
        self.assertEqual(character.endurance, 1)
        self.assertEqual(character.intelligence, 1)
        self.assertEqual(character.perception, 1)
        self.assertEqual(character.willpower, 1)
        self.assertEqual(character.charisma, 1)
        self.assertEqual(character.current_health, 0)
        self.assertEqual(character.current_stamina, 0)
        self.assertEqual(character.current_mana, 0)
        self.assertEqual(character.status, Character.Status.PENDING)
        self.assertEqual(character.owner, self.owner)

    def test_name_must_be_unique_for_same_owner(self):
        Character.objects.create(owner=self.owner, name="Akasha")

        with self.assertRaises(IntegrityError), transaction.atomic():
            Character.objects.create(owner=self.owner, name="Akasha")

    def test_different_owners_can_use_same_name(self):
        second_owner = get_user_model().objects.create_user(
            username="bob",
            email="bob@example.com",
            password="autre-mot-de-passe",
        )
        Character.objects.create(owner=self.owner, name="Akasha")

        character = Character.objects.create(owner=second_owner, name="Akasha")

        self.assertEqual(character.name, "Akasha")

    def test_database_rejects_duplicate_name_ignoring_case_and_spaces(self):
        Character.objects.create(owner=self.owner, name="Akasha")

        with self.assertRaises(IntegrityError), transaction.atomic():
            Character.objects.create(owner=self.owner, name="  akasha  ")

    def test_database_rejects_invalid_character_data(self):
        invalid_characters = (
            Character(owner=self.owner, name="A"),
            Character(owner=self.owner, name="Valid", level=0),
            Character(owner=self.owner, name="Valid", strength=0),
            Character(owner=self.owner, name="Valid", status="unknown"),
            Character(owner=self.owner, name="Valid", description="x" * 2001),
        )

        for character in invalid_characters:
            with self.subTest(character=character), self.assertRaises(
                IntegrityError
            ), transaction.atomic():
                character.save()


class CharacterApiTests(APITestCase):
    def setUp(self):
        self.owner = get_user_model().objects.create_user(
            username="alice",
            email="alice@example.com",
            password="mot-de-passe-solide",
        )
        self.other_user = get_user_model().objects.create_user(
            username="bob",
            email="bob@example.com",
            password="autre-mot-de-passe",
        )
        self.client.force_authenticate(self.owner)
        self.list_url = reverse("character-list")

    def test_create_and_list_character(self):
        create_response = self.client.post(
            self.list_url,
            {
                "name": "Akasha",
                "level": 3,
                "experience": 250,
                "description": "Archiviste des mondes oubliés.",
                "strength": 4,
                "agility": 5,
                "endurance": 6,
                "intelligence": 8,
                "perception": 7,
                "willpower": 6,
                "charisma": 5,
                "current_health": 30,
                "current_stamina": 20,
                "current_mana": 40,
                "status": Character.Status.ACTIVE,
            },
            format="json",
        )

        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(create_response.data["owner"], self.owner.pk)
        self.assertEqual(create_response.data["name"], "Akasha")

        list_response = self.client.get(self.list_url)
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_response.data), 1)

    def test_retrieve_update_and_delete_character(self):
        character = Character.objects.create(owner=self.owner, name="Akasha")
        detail_url = reverse("character-detail", args=(character.pk,))

        retrieve_response = self.client.get(detail_url)
        self.assertEqual(retrieve_response.status_code, status.HTTP_200_OK)

        update_response = self.client.patch(
            detail_url,
            {"level": 2, "experience": 100},
            format="json",
        )
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        character.refresh_from_db()
        self.assertEqual(character.level, 2)
        self.assertEqual(character.experience, 100)

        delete_response = self.client.delete(detail_url)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Character.objects.filter(pk=character.pk).exists())

    def test_user_cannot_access_another_users_character(self):
        character = Character.objects.create(owner=self.other_user, name="Secret")
        detail_url = reverse("character-detail", args=(character.pk,))

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"]["code"], "not_found")
        self.assertEqual(response.data["error"]["status"], 404)

    def test_api_requires_authentication(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(self.list_url)

        self.assertIn(
            response.status_code,
            (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN),
        )
        self.assertIn(
            response.data["error"]["code"],
            ("authentication_required", "permission_denied"),
        )

    def test_reject_duplicate_name_for_same_owner(self):
        Character.objects.create(owner=self.owner, name="Akasha")

        response = self.client.post(
            self.list_url,
            {"name": "Akasha"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"]["code"], "validation_error")
        self.assertIn("name", response.data["error"]["details"])

    def test_reject_invalid_character_values(self):
        response = self.client.post(
            self.list_url,
            {
                "name": "Akasha",
                "level": 0,
                "experience": -1,
                "strength": 0,
                "current_health": -1,
                "status": "unknown",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"]["status"], 400)
        self.assertIn("level", response.data["error"]["details"])
        self.assertIn("experience", response.data["error"]["details"])
        self.assertIn("strength", response.data["error"]["details"])
        self.assertIn("current_health", response.data["error"]["details"])
        self.assertIn("status", response.data["error"]["details"])

    def test_reject_duplicate_name_ignoring_case_and_spaces(self):
        Character.objects.create(owner=self.owner, name="Akasha")

        response = self.client.post(
            self.list_url,
            {"name": "  akasha  "},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data["error"]["details"])

    def test_clean_character_text_fields(self):
        response = self.client.post(
            self.list_url,
            {"name": "  Akasha  ", "description": "  Une archiviste  "},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Akasha")
        self.assertEqual(response.data["description"], "Une archiviste")

    def test_reject_short_name_and_long_description(self):
        response = self.client.post(
            self.list_url,
            {"name": "A", "description": "x" * 2001},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        details = response.data["error"]["details"]
        self.assertIn("name", details)
        self.assertIn("description", details)

    def test_reject_unsupported_http_method(self):
        response = self.client.put(self.list_url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response.data["error"]["code"], "method_not_allowed")
