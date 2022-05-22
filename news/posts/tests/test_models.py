from django.test import TestCase
from django.contrib.auth.models import User

from posts.models import Post, Comment, Tag, Category


class _AbstractModelTest:
    model = None

    def setUp(self):
        self.obj = self.model.objects.create(**{'title': 'test'})

    def tearDown(self):
        self.model.objects.all().delete()

    def test_object_str(self):
        self.assertEqual(self.obj.title, 'test')

    def test_retrieve(self):
        instance = self.model.objects.get(pk=self.obj.pk)
        self.assertEqual(instance.slug, self.obj.slug)
        self.assertEqual(instance.title, self.obj.title)


class PostModelTest(_AbstractModelTest, TestCase):
    model = Post


class TagModelTest(_AbstractModelTest, TestCase):
    model = Tag


class CategoryModelTest(_AbstractModelTest, TestCase):
    model = Category


class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', email='test@test.test', password='qwerty')
        self.post = Post.objects.create(title='test')
        self.comment = Comment.objects.create(**{'author_name': self.user, 'post': self.post})

    def tearDown(self):
        User.objects.all().delete()
        Post.objects.all().delete()
        Comment.objects.all().delete()

    def test_comment_str(self):
        self.assertEquals(str(self.comment), f'Comment by {self.user} on {self.post}')
