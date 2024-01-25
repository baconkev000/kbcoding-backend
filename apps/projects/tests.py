from backend.users.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token


class ProjectsTestCase(APITestCase):
    """Tests related to the Project models."""

    def setUp(self):
        """Set up required items for the tests."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="test",
            email="test@test.com",
            password="password",
        )

        self.superuser = User.objects.create_superuser(
            username="test_super",
            email="super@test.com",
            password="password",
        )
        self.token = Token.objects.create(user=self.user)

    def tearDown(self):
        """Delete things in the reverse of the order they were made"""
        self.superuser.delete()
        self.user.delete()

    def test_create_user(self):
        """Our user in setup is a user"""
        self.assertIsInstance(self.user, User)
        self.assertFalse(self.user.is_superuser)

    # Project Tests
    def test_get_project_list(self):
        """Can get list of all projects"""
        self.client.force_login(user=self.user)
        project_list_response = self.client.get(
            "/api/projects/",
            format="json",
        )
        self.assertEqual(project_list_response.status_code, status.HTTP_200_OK)

    def test_cannot_get_project_list_without_token(self):
        """Cannnot get list of all projects without an auth token"""
        project_list_response = self.client.get(
            "/api/projects/",
            format="json",
        )
        self.assertEqual(project_list_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_single_project(self):
        """Can get a single project by pk"""
        self.client.force_login(user=self.user)
        object_pk = 1
        player_list_response = self.client.get(
            f"/api/players/{object_pk}/",
            format="json",
        )
        self.assertEqual(player_list_response.status_code, status.HTTP_200_OK)

    # ProjectType Tests
    def test_get_project_type_list(self):
        """Can get list of all project types"""
        self.client.force_login(user=self.user)
        project_list_response = self.client.get(
            "/api/project_types/",
            format="json",
        )
        self.assertEqual(project_list_response.status_code, status.HTTP_200_OK)

    def test_get_single_project(self):
        """Can get a single project by pk"""
        self.client.force_login(user=self.user)
        object_pk = 1
        player_list_response = self.client.get(
            f"/api/players/{object_pk}/",
            format="json",
        )
        self.assertEqual(player_list_response.status_code, status.HTTP_200_OK)