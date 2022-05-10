import json

from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from posts.models import Post, UserPostRelation, Comment
from api.serializers import PostsSerializer


class PostsApiTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='test_user_1')
        self.post1 = Post.objects.create(title='test post 1', link='http://www.testpost1link.com',
                                         creation_date='2022-02-01')
        self.post2 = Post.objects.create(title='test post 2', link='http://www.testpost2link.com',
                                         creation_date='2022-01-02')
        self.assertEqual(self.post1.title, str(self.post1))

    def test_get_post_list(self):
        url = reverse('post-list')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(PostsSerializer([self.post1, self.post2], many=True).data, response.data)

    def test_post_create(self):
        self.client.force_login(self.user1)
        url = reverse('post-list')
        data = {
            "title": "test3",
            "link": "http://www.test3link.com",
            "creation_date": "2020-10-10",
            "amount_of_upvotes": 44
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(Post.objects.last().author_name, self.user1)

    def test_post_update(self):
        self.client.force_login(self.user1)
        url = reverse('post-detail', args=(self.post1.id,))
        data = {
            "title": 'some changed title',
            "link": self.post1.link,
            "creation_date": self.post1.created
        }
        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.post1.refresh_from_db()
        self.assertEqual(self.post1.title, 'some changed title')

    def test_get_post_detail(self):
        url = reverse('post-detail', args=(self.post1.id,))
        response = self.client.get(url)
        self.assertEqual(response.data['id'], self.post1.id)

    def test_post_delete(self):
        self.client.force_login(self.user1)
        self.assertEqual(2, Post.objects.all().count())
        url = reverse('post-detail', args=(self.post1.id,))
        response = self.client.delete(url, content_type='application/json')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(1, Post.objects.all().count())


class PostRelationTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='test_user_1')
        self.post1 = Post.objects.create(title='test post 1', link='http://www.testpost1link.com',
                                         creation_date='2022-02-01')
        self.post2 = Post.objects.create(title='test post 2', link='http://www.testpost2link.com',
                                         creation_date='2022-01-02')

    def test_upvote(self):
        url = reverse('userpostrelation-detail', args=(self.post1.id,))
        data = {
            "upvote": True
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user1)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserPostRelation.objects.get(user=self.user1, post=self.post1)
        self.assertTrue(relation.upvote)


class CommentsTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='test_user_1')
        self.user2 = User.objects.create(username='test_user_2')

        self.post1 = Post.objects.create(title='test post 1', link='http://www.testpost1link.com',
                                         creation_date='2022-02-01')
        self.post2 = Post.objects.create(title='test post 2', link='http://www.testpost2link.com',
                                         creation_date='2022-01-02')

    def test_comment(self):
        self.client.force_login(self.user1)
        url = reverse('comment-detail', args=(self.post1.id,))
        data = {
            "content": "some comment content",
            "creation_date": "2020-10-01",

        }
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        comment = Comment.objects.get(user=self.user1, post=self.post1)
        self.post1.refresh_from_db()
        self.assertEqual(comment.content, "some comment content")
