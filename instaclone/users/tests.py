from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework import status


class AuthenticateBaseTestCase(APITestCase):
    def authenticate(self):
        self.client.post(reverse("create_user_api"), {
            "username": "test",
            "password": "password"
        })

        response = self.client.post(reverse("login_api"), {
            "username": "test",
            "password": "password"
        })

        if not response.data.get("access"):
            token = response.data.get("data").get("access")
        else:
            token = response.data.get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")


class CreateUserTestCase(AuthenticateBaseTestCase):
    def test_add_user(self):
        test_data = {
            "username": "test",
            "password": "test",
            "email": "test@gmail.com"
        }

        response = self.client.post(reverse("create_user_api"), data=test_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["errors"], "")


class ListUsersTestCase(AuthenticateBaseTestCase):
    def test_list_users(self):
        self.authenticate()

        response = self.client.get("/users/list/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserProfileDetailTestCase(AuthenticateBaseTestCase):
    def setUp(self):
        self.authenticate()
        test_data = {
            "username": "test1",
            "password": "test",
            "email": "test@gmail.com"
        }

        self.client.post(reverse("create_user_api"), data=test_data)

    def test_get_user_profile_detail(self):
        self.authenticate()
        response = self.client.get("/users/1/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_profile_detail(self):
        self.authenticate()

        test_data = {
            "first_name": "test_updated_username",
            "last_name": "test_updated_lastname",
            "bio": "updated bio"
        }
        response = self.client.put("/users/1/", data=test_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["bio"], "updated bio")


class UserNetworkEdgeViewTestCase(AuthenticateBaseTestCase):
    def setUp(self):
        self.url = reverse("user_network_edge_api")
        self.authenticate()
        test_data1 = {
            "username": "test1",
            "password": "test",
            "email": "test1@gmail.com"
        }

        self.client.post(reverse("create_user_api"), data=test_data1)

    def test_follow_a_user(self):
        self.authenticate()
        data = {
            "to_user": 2
        }
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_list_of_following(self):
        self.authenticate()
        data = {
            "direction": "following"
        }
        response = self.client.get(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list_of_followers(self):
        self.authenticate()
        data = {
            "direction": "followers"
        }
        response = self.client.get(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unfollow_user(self):
        self.authenticate()
        data = {
             "to_user": 2
        }
        response = self.client.delete(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
