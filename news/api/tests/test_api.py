import json

from api.views import PostViewSet
from core.models import User
from django.urls import reverse, reverse_lazy

from rest_framework.test import APITestCase
from rest_framework import status

from posts.models import Post, Comment, Category
from api.serializers import PostSerializer
from rest_framework.test import APIRequestFactory


class PostsApiTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='test_user_1')
        self.post1 = Post.objects.create(title='test post 1', created='2022-02-01')
        self.post2 = Post.objects.create(title='test post 2', created='2022-01-02')
        self.category1 = Category.objects.create(title='test category', created='2022-01-02')
        self.assertEqual(self.post1.title, str(self.post1))

    def test_get_post_list(self):
        url = '/api/v1/posts/'
        # import ipdb
        # ipdb.set_trace()
        # url = reverse('posts')  # TODO: resolve reverse or reverse_lazy
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(PostSerializer([self.post2, self.post1], many=True).data, response.data)

    def test_post_create(self):
        self.client.force_login(self.user1)
        url = '/api/v1/posts/'
        data = {
            "title": "test228",
            "content": "test content",
            "author_name": self.user1,
            "category": self.category1.pk,
            "tags": "test1, test2"
        }
        # json_data = json.dumps(data)

        # import ipdb
        # ipdb.set_trace()
        # response = self.client.post(url, data=json_data, content_type='application/json')
        response = self.client.post(url, data=data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(Post.objects.get(title='test228').author_name, self.user1)

    def test_post_update(self):
        self.client.force_login(self.user1)
        # url = reverse('post-detail', args=(self.post1.id,))
        url = '/api/v1/posts/' + self.post1.slug
        data = {
            "title": 'some changed title',
        }
        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data, content_type='application/json')
        # self.assertEqual(status.HTTP_200_OK, response.status_code)
        # self.post1.refresh_from_db()
        # self.assertEqual(self.post1.title, 'some changed title')

    # def test_get_post_detail(self):
    #     url = reverse('posts-detail', args=(self.post1.id,))
    #     response = self.client.get(url)
    #     self.assertEqual(response.data['id'], self.post1.id)
    #
    # def test_post_delete(self):
    #     self.client.force_login(self.user1)
    #     self.assertEqual(2, Post.objects.all().count())
    #     url = reverse('post-detail', args=(self.post1.id,))
    #     response = self.client.delete(url, content_type='application/json')
    #     self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
    #     self.assertEqual(1, Post.objects.all().count())


#
#
# class PostRelationTestCase(APITestCase):
#     def setUp(self):
#         self.user1 = User.objects.create(username='test_user_1')
#         self.post1 = Post.objects.create(title='test post 1', link='http://www.testpost1link.com',
#                                          creation_date='2022-02-01')
#         self.post2 = Post.objects.create(title='test post 2', link='http://www.testpost2link.com',
#                                          creation_date='2022-01-02')
#
#     def test_upvote(self):
#         url = reverse('userpostrelation-detail', args=(self.post1.id,))
#         data = {
#             "upvote": True
#         }
#         json_data = json.dumps(data)
#         self.client.force_login(self.user1)
#         response = self.client.patch(url, data=json_data, content_type='application/json')
#         self.assertEqual(status.HTTP_200_OK, response.status_code)
#         relation = UserPostRelation.objects.get(user=self.user1, post=self.post1)
#         self.assertTrue(relation.upvote)
#
#
class CommentsTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='test_user_11', email='test_user_email1')
        self.user2 = User.objects.create(username='test_user_22', email='test_user_email2')

        self.post1 = Post.objects.create(title='test post 1', created='2022-02-01')
        self.post2 = Post.objects.create(title='test post 2', created='2022-01-02')

    # def test_comment(self):
    #     self.client.force_login(self.user1)
    #     url = reverse('comment-detail', args=(self.post1.id,))
    #     data = {
    #         "content": "some comment content",
    #         "created": "2020-10-01",
    #
    #     }
    #     json_data = json.dumps(data)
    #     response = self.client.patch(url, data=json_data, content_type='application/json')
    #     self.assertEqual(status.HTTP_200_OK, response.status_code)
    #     comment = Comment.objects.get(user=self.user1, post=self.post1)
    #     self.post1.refresh_from_db()
    #     self.assertEqual(comment.content, "some comment content")
