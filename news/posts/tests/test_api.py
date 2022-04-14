from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from posts.models import Post
from posts.serializers import PostsSerializer


class PostsApiTestCase(APITestCase):
    def test_get(self):
        post1 = Post.objects.create(title='test post 1', link='testpost1link.com', creation_date='2022-02-01',
                                    amount_of_upvotes='33')
        post2 = Post.objects.create(title='test post 2', link='testpost2link.com', creation_date='2022-01-02',
                                    amount_of_upvotes='23')
        url = reverse('post-list')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(PostsSerializer([post1, post2], many=True).data, response.data)
