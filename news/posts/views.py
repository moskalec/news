from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator

from slugify import slugify

from posts.forms import CreatePostForm, CreateCommentForm
from posts.models import Post, Category, Comment, Tag


class HomePageView(TemplateView):
    template_name = "posts/index.tpl"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_posts'] = Post.latest.all()
        context['featured_post'] = Post.featured.all()
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        context['section'] = 'home'
        return context


class CategoriesListView(ListView):
    model = Category


class CategoryDetailView(DetailView):
    model = Category


class PostsListView(ListView):
    model = Post
    paginate_by = 3

    def get_context_data(self, **kwargs):
        if 'category_slug' in self.kwargs:
            category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
            posts = Post.objects.all().filter(category=category).order_by('-created')
            section = 'by_category'
        elif 'tag_slug' in self.kwargs:
            tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
            posts = Post.objects.all().filter(tags__slug__contains=tag).order_by('-created')
            section = 'by_tag'
        else:
            posts = Post.objects.all().order_by('-created')
            section = 'all_posts'
        context = super().get_context_data(object_list=posts, **kwargs)
        context['section'] = section
        context['latest_posts'] = Post.objects.all()[:5]
        return context

    @method_decorator(login_required)
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
                return redirect(request.POST.get('current'))
            except Exception:
                pass


class PostDetailView(DetailView):
    model = Post
    form_class = CreateCommentForm
    template_name = 'posts/post_detail.html'

    @method_decorator(login_required)
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
            except Exception:
                pass
            return redirect(request.POST.get('current'))

        form = self.form_class()
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
        return render(request, self.template_name, {'form': form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(active=True, post_id=self.object.id)
        context['comment_form'] = self.form_class()
        return context


@login_required
def post_create(request):
    if request.method == 'POST':
        form = CreatePostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.author_name = request.user
            tags = []
            for tag in request.POST.dict()['tags'].split(","):
                obj, _ = Tag.objects.get_or_create(title=tag.strip(), slug=slugify(tag.strip()))
                tags.append(obj)
            new_item.save()
            new_item.tags.add(*tags)
            messages.success(request, 'Post added successfully')
            return redirect(new_item)
    else:
        form = CreatePostForm(data=request.GET)
    return render(request,
                  'posts/create.html',
                  {'form': form,
                   'section': 'create_post'})

# @require_POST
# def like_dislike(request):
#     if request.method == "POST":
#         post_id = request.POST.get('post_id')
#         action = request.POST.get('action')
#         if post_id and action:
#             try:
#                 post = Post.objects.get(id=post_id)
#                 if action == 'like':
#                     if post.like.filter(username=request.user.username).exists():
#                         post.like.remove(request.user)
#                     else:
#                         post.like.add(request.user)
#                         post.dislike.remove(request.user)
#                 elif action == 'dislike':
#                     if post.dislike.filter(username=request.user.username).exists():
#                         post.dislike.remove(request.user)
#                     else:
#                         post.dislike.add(request.user)
#                         post.like.remove(request.user)
#                 # return HttpResponseRedirect(post.get_absolute_url())
#                 return redirect(request.path_info)
#             except Exception:
#                 pass
#         return HttpResponseRedirect(reverse('posts:index'))
