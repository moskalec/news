from django.test import TestCase
from rest_framework import status

from posts.models import Post
from api.serializers import PostSerializer
from core.models import User


class PostSerializerTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='test_user01', email='testuser01@mail.com')
        self.user2 = User.objects.create(username='test_user02', email='testuser02@mail.com')

        self.post1 = Post.objects.create(title='test post 1', created='2022-02-01', author_name=self.user1)
        self.post2 = Post.objects.create(title='test post 2', created='2022-01-02', author_name=self.user2)

    def tearDown(self):
        User.objects.all().delete()
        Post.objects.all().delete()

    def test_post(self):

        data = PostSerializer([self.post2, self.post1], many=True).data

        response = self.client.get('/api/v1/posts/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(data, response.data)
