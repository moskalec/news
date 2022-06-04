from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import UserEditForm, ProfileEditForm, UserRegistrationForm  # , PasswordResetForm
from .models import Profile, Contact
from django.contrib import messages
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import login
from django.views.generic.edit import UpdateView
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationView(CreateView):
    template_name = 'account/user/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('account:dashboard')

    def form_valid(self, form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = User.objects.get(username=cd['username'])
        Profile.objects.create(user=user)

        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return result


@login_required
def dashboard(request):
    context = {
        'section': 'people',
        'followers': Contact.objects.filter(user_to=request.user)
    }
    return render(request,
                  'account/dashboard.html',
                  context=context)


class UserProfileEditView(UpdateView):
    template_name = 'account/edit.html'
    model = get_user_model()
    exclude = ('password',)
    form_class = UserEditForm

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, username=self.request.user.username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserEditForm(instance=self.object)
        context['profile_form'] = ProfileEditForm(instance=self.object.profile)
        return context

    def post(self, request, *args, **kwargs):
        context = super().post(request)
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
        return context


class UserDetailView(DetailView):
    template_name = 'account/user/detail.html'
    model = get_user_model()
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'people'
        context['followers'] = Contact.objects.filter(user_to=self.get_object())
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
