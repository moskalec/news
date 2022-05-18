from django import forms
from .models import Post, Comment
from django.utils.translation import gettext_lazy as _
from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify


class CreatePostForm(forms.ModelForm):
    tags = forms.CharField(max_length=100)

    def save(self, force_insert=False,
             force_update=False,
             commit=True):
        post = super().save(commit=False)
        image_url = self.cleaned_data['url']
        if image_url is not None:
            name = slugify(post.title)
            extension = image_url.rsplit('.', 1)[1].lower()
            response = request.urlopen(image_url)
            image_name = f'{name}.{extension}'
            post.image.save(image_name, ContentFile(response.read()), save=False)
        if commit:
            post.save()

        return post

    def clean_url(self):
        url = self.cleaned_data['url']
        if url is not None:
            valid_extensions = ['jpg', 'jpeg']
            extension = url.rsplit('.', 1)[1].lower()
            if extension not in valid_extensions:
                raise forms.ValidationError('The given URL does not match valid image extensions.')
        return url

    class Meta:
        model = Post
        fields = ('title', 'content', 'image', 'url')
        widgets = {'url': forms.HiddenInput}
        labels = {
            'title': _('Title'),
            'content': _('Content'),
            'image': _('Image'),
            'tags': _('Tags'),
        }
        help_texts = {
            'title': _('Title'),
            'content': _('Content'),
            'image': _('Image'),
            'tags': _('Enter tags separated by commas'),
        }
        error_messages = {
            'title': {
                'max_length': _("This title is too long."),
            },
        }

    def __init__(self, *args, **kwargs):
        super(CreatePostForm, self).__init__(*args, **kwargs)

        self.fields['title'].widget.attrs['placeholder'] = _('Enter post title')
        self.fields['content'].widget.attrs['placeholder'] = _('Enter content')
        self.fields['image'].widget.attrs['placeholder'] = _('Choose image')
        self.fields['tags'].widget.attrs['placeholder'] = _('Enter tags separated by commas')


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
