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

        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")


# Create your tests here.
class UserPostCreateFeedTestCase(AuthenticateBaseTestCase):
    def setUp(self) -> None:
        self.url = reverse('user_post_view')

    def test_list_posts(self):
        self.authenticate()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_posts(self):
        self.authenticate()

        test_data = {
            "caption_text": "Testing data",
            "location": "Test location",
            "is_published": True
        }
        response = self.client.post(self.url, test_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["caption_text"], "Testing data")
        self.assertEqual(response.data["location"], "Test location")
        self.assertEqual(response.data["is_published"], True)


class UserPostDetailUpdateViewTestCase(AuthenticateBaseTestCase):
    def setUp(self) -> None:
        self.authenticate()

        test_data = {
            "caption_text": "Testing data",
            "location": "Test location",
            "is_published": True
        }
        self.client.post(reverse('user_post_view'), test_data)

    def test_get_post(self):
        self.authenticate()

        response = self.client.get('/post/1/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_user_post(self):
        self.authenticate()

        test_data = {
            "caption_text": "My First Post",
            "location": "Kolhapur, Maharashtra",
            "is_published": True
        }
        response = self.client.put('/post/2/', data=test_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["caption_text"], "My First Post")


class PostLikeViewSetTestCase(AuthenticateBaseTestCase):
    def setUp(self) -> None:
        self.authenticate()

        test_data = {
            "caption_text": "Testing data",
            "location": "Test location",
            "is_published": True
        }
        self.client.post(reverse('user_post_view'), test_data)

    def test_list_post_likes(self):
        self.authenticate()
        response = self.client.get('/post/like/', data={"post_id": 1})
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_like_a_post(self):
        self.authenticate()
        post_data = {
            "post": 1
        }
        response = self.client.post("/post/like/", data=post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_remove_like_on_a_post(self):
        self.authenticate()
        post_data = {
            "post": 1
        }
        response = self.client.delete("/post/like/", data=post_data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class PostCommentViewSetTestCase(AuthenticateBaseTestCase):
    def setUp(self) -> None:
        self.authenticate()

        test_data = {
            "caption_text": "Testing data",
            "location": "Test location",
            "is_published": True
        }
        self.client.post(reverse('user_post_view'), test_data)

    def test_create_comment_on_a_post(self):
        self.authenticate()

        test_data = {
            "post": 1,
            "text": "Test comment !"
        }

        response = self.client.post('/post/comment/', data=test_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["text"], "Test comment !")

    def test_list_comments_on_a_post(self):
        self.authenticate()

        response = self.client.get('/post/comment/', data={"post_id": 1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
