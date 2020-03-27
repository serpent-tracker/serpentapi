import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from profiles.api.serializers import ProfileStatusSerializer
from profiles.models import ProfileStatus


class RegistrationTestCase(APITestCase):
    def test_registration(self):
        data = {
            "username": "testcase",
            "email": "test@localhost.app",
            "password1": "some_strong_psw",
            "password2": "some_strong_psw",
        }
        response = self.client.post("/api/v1/rest-auth/registration/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ProfileViewSetTestCase(APITestCase):

    list_url = reverse("profiles-list")

    def setUp(self):
        self.user = User.objects.create_user(username="woz", password="some-verry-strong-psw")
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_profile_list_authenticated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_list_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_profile_detail_retrieve(self):
        response = self.client.get(reverse("profiles-detail", kwargs={"pk": self.user.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"], "woz")

    def test_profile_update_by_owner(self):
        response = self.client.put(
            reverse("profiles-detail", kwargs={"pk": self.user.pk}), {"city": "Raleigh", "bio": "Test Bio..."},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content),
            {"id": self.user.id, "user": "woz", "bio": "Test Bio...", "city": "Raleigh", "avatar": None,},
        )

    def test_profile_update_by_rando(self):
        rando = User.objects.create_user(username="rando", password="psw123123123")
        self.client.force_authenticate(user=rando)
        response = self.client.put(reverse("profiles-detail", kwargs={"pk": self.user.pk}), {"bio": "hacked!!!"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ProfileStatusViewSetTestCase(APITestCase):

    url = reverse("status-list")

    def setUp(self):
        self.user = User.objects.create_user(username="woz", password="some-verry-strong-psw")
        self.status = ProfileStatus.objects.create(user_profile=self.user.profile, status_content="status test")
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_status_list_authenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_status_list_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_status_create(self):
        data = {"status_content": "a new status!"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["user_profile"], "woz")
        self.assertEqual(response.data["status_content"], "a new status!")

    def test_single_status_retrive(self):
        serializer_data = ProfileStatusSerializer(instance=self.status).data
        response = self.client.get(reverse("status-detail", kwargs={"pk": self.user.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)
        self.assertEqual(serializer_data, response_data)

    def test_status_update_owner(self):
        data = {"status_content": "content updated"}
        response = self.client.put(reverse("status-detail", kwargs={"pk": self.status.pk}), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status_content"], "content updated")

    def test_status_update_rando_user(self):
        rando = User.objects.create_user(username="rando", password="psw123123123")
        self.client.force_authenticate(user=rando)
        data = {"status_content": "All Your Profiles Are Belong To Us"}
        response = self.client.put(reverse("status-detail", kwargs={"pk": self.status.pk}), data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)