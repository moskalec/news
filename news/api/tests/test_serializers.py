# from unittest import TestCase
#
# from posts.models import Post, UserPostRelation
# from api.serializers import PostsSerializer
# from django.contrib.auth.models import User
#
#
# class PostSerializerTestCase(TestCase):
#     def test_post(self):
#         self.user1 = User.objects.create(username='testuser1')
#         self.user2 = User.objects.create(username='testuser2')
#
#         post1 = Post.objects.create(title='test post 1', link='http://www.testpost1link.com',
#                                     creation_date='2022-02-01', author_name=self.user1)
#         post2 = Post.objects.create(title='test post 2', link='http://www.testpost2link.com',
#                                     creation_date='2022-01-02', author_name=self.user2)
#
#         UserPostRelation.objects.create(user=self.user1, post=post1, upvote=True)
#         UserPostRelation.objects.create(user=self.user2, post=post1, upvote=True)
#         data = PostsSerializer([post1, post2], many=True).data
#
#         expected_data = [
#             {
#                 'id': post1.id,
#                 'title': 'test post 1',
#                 'link': 'http://www.testpost1link.com',
#                 'creation_date': '2022-02-01',
#                 'author_name': self.user1.id,
#                 'amount_of_upvotes': 2,
#             },
#             {
#                 'id': post2.id,
#                 'title': 'test post 2',
#                 'link': 'http://www.testpost2link.com',
#                 'creation_date': '2022-01-02',
#                 'author_name': self.user2.id,
#                 'amount_of_upvotes': 0,
#             }
#         ]
#         self.assertEqual(data, expected_data)
