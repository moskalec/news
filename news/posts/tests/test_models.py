from django.test import TestCase
from django.contrib.auth.models import User

from posts.models import Post, Comment, Tag, Category


class __AbstractModelTest(TestCase):
    model = None

    def setUp(self):
        self.obj = self.model.objects.create(**{'title': 'test'})

    def tearDown(self):
        self.model.objects.all().delete()


class _TestBasicFunctionalityMixin:
    def test_object_str(self):
        self.assertEqual(self.obj.title, 'test')

    def test_retrieve(self):
        instance = self.model.objects.get(pk=self.obj.pk)
        self.assertEqual(instance.slug, self.obj.slug)
        self.assertEqual(instance.title, self.obj.title)


class PostModelTest(__AbstractModelTest, _TestBasicFunctionalityMixin):
    model = Post


class TagModelTest(__AbstractModelTest, _TestBasicFunctionalityMixin):
    model = Tag


class CategoryModelTest(__AbstractModelTest, _TestBasicFunctionalityMixin):
    model = Category


class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', email='test@test.test', password='qwerty')
        self.post = Post.objects.create(title='test')
        self.comment = Comment.objects.create(**{'user': self.user, 'post': self.post})

    def test_comment_str(self):
        self.assertEquals(str(self.comment), f'Comment by {self.user} on {self.post}')
