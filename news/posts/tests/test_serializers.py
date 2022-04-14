from unittest import TestCase

from posts.models import Post
from posts.serializers import PostsSerializer


class PostSerializerTestCase(TestCase):
    def test_post(self):
        post1 = Post.objects.create(title='test post 1', link='testpost1link.com', creation_date='2022-02-01',
                                    amount_of_upvotes='33')
        post2 = Post.objects.create(title='test post 2', link='testpost2link.com', creation_date='2022-01-02',
                                    amount_of_upvotes='23')
        data = PostsSerializer([post1, post2], many=True).data

        expected_data = [
            {
                'id': post1.id,
                'title': 'test post 1',
                'link': 'testpost1link.com',
                'creation_date': '2022-02-01',
                'amount_of_upvotes': 33
            },
            {
                'id': post2.id,
                'title': 'test post 2',
                'link': 'testpost2link.com',
                'creation_date': '2022-01-02',
                'amount_of_upvotes': 23
            }
        ]
        self.assertEqual(data, expected_data)