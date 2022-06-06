from django.test import TestCase, TransactionTestCase
from django.urls import reverse
from core.models import User

from posts.forms import CreateCommentForm
from posts.models import Post, Tag, Category


class _AbstractViewTest:
    model = None
    url_kwargs = None
    tpl_name = None

    def setUp(self):
        post1 = Post.objects.create(**{'title': 'test'})
        post2 = Post.objects.create(**{'title': 'test'})
        post3 = Post.objects.create(**{'title': 'test'})
        self.obj = self.model.objects.create(**{'title': f'{self.model.__name__.lower()}-test'})

    def tearDown(self):
        self.model.objects.all().delete()

    def test_absolute_url(self):
        response = self.client.get(reverse(self.tpl_name, kwargs=self.url_kwargs))
        self.assertEqual(response.status_code, 200)


class TagViewsTest(_AbstractViewTest, TestCase):
    model = Tag
    url_kwargs = {'slug': 'tag-test'}
    tpl_name = 'posts:tag-detail'


class CategoryViewsTest(_AbstractViewTest, TestCase):
    model = Category
    url_kwargs = {'slug': 'category-test'}
    tpl_name = 'posts:category-detail'

    def test_page_context(self):
        response = self.client.get(reverse(self.tpl_name, kwargs=self.url_kwargs))
        self.assertEqual(response.status_code, 200)


class PostsViewsTest(_AbstractViewTest, TestCase):
    model = Post
    tpl_name = 'posts:post-list'


class PostDetailViewsTest(_AbstractViewTest, TestCase):
    model = Post
    url_kwargs = {'slug': 'post-test'}
    tpl_name = 'posts:post-detail'


class PostDetailLikeDislikeTest(TransactionTestCase):
    model = Post
    url_kwargs = {'slug': 'post-test'}
    tpl_name = 'posts:post-detail'

    def setUp(self):
        self.user = User.objects.create_user(username='test', email='test@test.test', password='qwerty')
        self.post = Post.objects.create(title='test')

    def test_like_not_auth(self):
        url = reverse(self.tpl_name, kwargs=self.url_kwargs)
        self.assertEqual(self.post.like.count(), 0)

        response_post = self.client.post(path=url, data={'post_id': self.post.id, 'action': 'like', 'current': url})
        self.assertEqual(response_post.status_code, 302)
        self.post.refresh_from_db()
        self.assertEqual(self.post.like.count(), 0)

    def test_like_auth(self):
        url = reverse(self.tpl_name, kwargs=self.url_kwargs)
        self.assertEqual(self.post.like.count(), 0)

        self.client.force_login(self.user)
        response_post = self.client.post(path=url, data={'post_id': self.post.id, 'action': 'like', 'current': url})
        self.assertEqual(response_post.status_code, 302)
        self.post.refresh_from_db()
        self.assertEqual(self.post.like.count(), 1)

        response_post = self.client.post(path=url, data={'post_id': self.post.id, 'action': 'like', 'current': url})
        self.assertEqual(response_post.status_code, 302)
        self.post.refresh_from_db()
        self.assertEqual(self.post.like.count(), 0)

    def test_dislike_not_auth(self):
        url = reverse(self.tpl_name, kwargs=self.url_kwargs)
        self.assertEqual(self.post.dislike.count(), 0)

        response_post = self.client.post(path=url, data={'post_id': self.post.id, 'action': 'dislike', 'current': url})
        self.assertEqual(response_post.status_code, 302)
        self.post.refresh_from_db()
        self.assertEqual(self.post.dislike.count(), 0)

    def test_dislike_auth(self):
        url = reverse(self.tpl_name, kwargs=self.url_kwargs)
        self.assertEqual(self.post.dislike.count(), 0)

        self.client.force_login(self.user)
        response_post = self.client.post(path=url, data={'post_id': self.post.id, 'action': 'dislike', 'current': url})
        self.assertEqual(response_post.status_code, 302)
        self.post.refresh_from_db()
        self.assertEqual(self.post.dislike.count(), 1)

        response_post = self.client.post(path=url, data={'post_id': self.post.id, 'action': 'dislike', 'current': url})
        self.assertEqual(response_post.status_code, 302)
        self.post.refresh_from_db()
        self.assertEqual(self.post.dislike.count(), 0)

    def test_like_exception(self):
        url = reverse(self.tpl_name, kwargs=self.url_kwargs)
        self.client.force_login(self.user)
        self.assertEqual(self.post.like.count(), 0)
        self.client.post(path=url, data={'post_id': self.post.id, 'action': 'test', 'current': url})
        self.assertEqual(self.post.like.count(), 0)


class PostListLikeDislikeTest(PostDetailLikeDislikeTest):
    model = Post
    url_kwargs = ''
    tpl_name = 'posts:post-list'


class PostCommentTest(TestCase):
    model = Post
    url_kwargs = {'slug': 'post-test'}
    tpl_name = 'posts:post-detail'

    def setUp(self):
        self.user = User.objects.create_user(username='test', email='test@test.test', password='qwerty')
        self.post = Post.objects.create(title='post-test')
        self.post2 = Post.objects.create(title='test')
        self.post3 = Post.objects.create(title='test-1')

    def test_form(self):
        self.client.force_login(self.user)
        form_data = {
            'content': 'test'
        }
        form = CreateCommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_comment(self):
        self.assertEqual(self.post.comments.count(), 0)

        self.client.force_login(self.user)
        url = reverse(self.tpl_name, kwargs=self.url_kwargs)
        form_data = {
            'content': 'test',
            'action': 'comment'
        }
        self.client.post(path=url, data=form_data)
        self.assertEqual(self.post.comments.count(), 1)
        self.assertEqual(self.post.comments.first().author_name, self.user)

        form_data = {
            'content': 'test',
            'action': 'comment',
            'parent_id': self.post.comments.last().id
        }
        self.client.post(path=url, data=form_data)
        self.assertEqual(self.post.comments.count(), 2)
        self.assertEqual(self.post.comments.last().author_name, self.user)
        self.assertEqual(self.post.comments.last().id, 2)
        self.assertEqual(self.post.comments.last().parent_id, self.post.comments.first().id)

        response = self.client.get(url)

        self.assertEqual(response.context['comments'].count(), 2)
        self.assertContains(response, 'form')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_detail.html')
        self.assertIsInstance(response.context['form'], CreateCommentForm)

        self.client.post(path=url, data={})
        self.assertEqual(response.status_code, 200)


class HomeViewTest(TestCase):
    def setUp(self):
        self.category1 = Category.objects.create(title='title_category1')
        self.category2 = Category.objects.create(title='title_category2')

        self.post1 = Post.objects.create(title='title_post1', category=self.category1)
        self.post2 = Post.objects.create(title='title_post2', category=self.category1)
        self.post3 = Post.objects.create(title='title_post3')
        self.post4 = Post.objects.create(title='title_post4', category=self.category1)
        self.post5 = Post.objects.create(title='title_post5')

        self.tag1 = self.post1.tags.create(title='title_tag1')
        self.tag2 = self.post1.tags.create(title='title_tag2')
        self.tag3 = Tag.objects.create(title='title_tag3')

    def test_home_page(self):
        response = self.client.get(reverse('posts:index'))
        categories = Category.objects.all().order_by('-title')
        tags = Tag.objects.all().order_by('-title')
        posts = Post.objects.all().order_by('-title')[:5]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['section'], 'home')
        self.assertEqual(response.context['featured_post'], self.post5)
        self.assertEqual(response.context['categories'].first(), categories.first())
        self.assertEqual(response.context['categories'].last(), categories.last())
        self.assertEqual(response.context['tags'].first(), tags.first())
        self.assertEqual(response.context['tags'].last(), tags.last())
        self.assertEqual(response.context['latest_posts'].first(), posts[0])
