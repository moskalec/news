from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.conf import settings

from posts.forms import CreatePostForm, CreateCommentForm
from posts.models import Post, Category, Comment, Tag
import redis

r = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB
)


class BasePageViewMixin(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_posts'] = Post.latest.all()
        context['featured_post'] = Post.objects.order_by('-total_likes').first()
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        context['section'] = 'home'
        return context


class HomePageView(BasePageViewMixin):
    template_name = "posts/index.tpl"


class OwnerMixin(object):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(author_name=self.request.user)


class OwnerEditMixin(object):
    def form_valid(self, form):
        form.instance.author_name = self.request.user
        return super().form_valid(form)


class OwnerPostMixin(OwnerMixin, LoginRequiredMixin):
    model = Post
    success_url = reverse_lazy('posts:manage_post_list')


class OwnerPostEditMixin(OwnerPostMixin, OwnerEditMixin):
    form_class = CreatePostForm
    template_name = 'posts/manage/post/form.html'


class ManagePostListView(OwnerPostMixin, ListView):
    template_name = 'posts/manage/post/list.html'


class PostCreateView(OwnerPostEditMixin, CreateView):
    pass


class PostUpdateView(OwnerPostEditMixin, UpdateView):
    def get_initial(self):
        tags = ", ".join(self.object.tags.values_list('title', flat=True))
        return {'tags': tags}


class PostDeleteView(OwnerPostMixin, DeleteView):
    template_name = 'posts/manage/post/delete.html'


class LikeDislikeMixin:
    def post(self, request, *args, **kwargs):
        post_id = request.POST.get('post_id')
        action = request.POST.get('action')
        if post_id and action:
            try:
                post = Post.objects.get(id=post_id)
                if action == 'like':
                    if post.like.filter(username=request.user.username).exists():
                        post.like.remove(request.user)
                    else:
                        post.like.add(request.user)
                        post.dislike.remove(request.user)
                elif action == 'dislike':
                    if post.dislike.filter(username=request.user.username).exists():
                        post.dislike.remove(request.user)
                    else:
                        post.dislike.add(request.user)
                        post.like.remove(request.user)
                return redirect(request.path_info)
            except Exception:
                pass
        return HttpResponseRedirect(reverse('posts:index'))


class PostsListView(ListView, LikeDislikeMixin):
    model = Post
    paginate_by = 3


class PostDetailView(DetailView, LikeDislikeMixin):
    model = Post
    form_class = CreateCommentForm
    template_name = 'posts/post_detail.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class()
        if request.POST.get('post_id'):
            return super().post(request, *args, **kwargs)
        if request.POST.get('action') == 'comment':
            action = request.POST.get('action')
            if action and action == 'comment':
                form = self.form_class(request.POST)
                if form.is_valid():
                    try:
                        parent_id = int(request.POST.get('parent_id'))
                    except Exception:
                        parent_id = None
                    if parent_id:
                        parent_obj = Comment.objects.get(id=parent_id)
                        if parent_obj:
                            replay_comment = form.save(commit=False)
                            replay_comment.parent = parent_obj
                    new_comment = form.save(commit=False)
                    new_comment.post = self.get_object()
                    new_comment.author_name = request.user
                    new_comment.save()

                    return HttpResponseRedirect(self.request.path_info)
                return HttpResponseRedirect(self.request.path_info)
            return HttpResponseRedirect(self.request.path_info)
        return render(request, self.template_name, {'comment_form': form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(active=True, post_id=self.object.id)
        context['comment_form'] = self.form_class()
        context['total_views'] = r.incr(f'post:{self.get_object().id}:views')
        r.zincrby('post_ranking', 1, self.get_object().id)
        return context


class CategoriesListView(ListView):
    model = Category


class CategoryDetailView(DetailView):
    model = Category


class TagsListView(ListView):
    model = Tag


class TagDetailView(DetailView):
    model = Tag
