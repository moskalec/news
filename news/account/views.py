from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile, Contact
from django.contrib import messages
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect
from django.urls import reverse


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def dashboard(request):
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard'})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(
            instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})


# @require_POST
# def user_follow(request):
#     if request.method == "POST":
#         user_id = request.POST.get('user_id')
#         action = request.POST.get('action')
#         if user_id and action:
#             try:
#                 user = User.objects.get(id=user_id)
#                 if action == 'follow':
#                     Contact.objects.get_or_create(
#                         user_from=request.user,
#                         user_to=user)
#                 else:
#                     Contact.objects.filter(user_from=request.user,
#                                            user_to=user).delete()
#                 return HttpResponseRedirect(user.get_absolute_url())
#             except Exception:
#                 pass
#         return HttpResponseRedirect(reverse('posts:index'))


class UserDetailView(DetailView):
    template_name = 'account/user/detail.html'
    model = User
    slug_field = 'username'

    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')
        if user_id and action:
            try:
                user = User.objects.get(id=user_id)
                if request.user == user:
                    return HttpResponseRedirect(user.get_absolute_url())
                if action == 'follow':
                    Contact.objects.get_or_create(
                        user_from=request.user,
                        user_to=user)
                else:
                    Contact.objects.filter(user_from=request.user,
                                           user_to=user).delete()
                return HttpResponseRedirect(user.get_absolute_url())
            except Exception:
                pass
        return HttpResponseRedirect(reverse('posts:index'))

    # def get_queryset(self):
    # user = get_object_or_404(User, username=self.args['username'])
    # return user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'people'
        return context


class UserListView(ListView):
    template_name = 'account/user/list.html'
    model = User
    queryset = User.objects.filter(is_active=True)
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'people'
        return context
