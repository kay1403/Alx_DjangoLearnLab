from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Tag
from django import forms
from .models import Comment


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class PostForm(forms.ModelForm):
    tag_names = forms.CharField(required=False, help_text="Comma separated tags")

    class Meta:
        model = Post
        fields = ['title', 'content', 'tag_names']

    def save(self, commit=True, user=None):
        post = super().save(commit=False)
        if user:
            post.author = user
        if commit:
            post.save()
            tag_names = self.cleaned_data.get('tag_names')
            if tag_names:
                tags = tag_names.split(',')
                for tag in tags:
                    tag_obj, created = Tag.objects.get_or_create(name=tag.strip())
                    post.tags.add(tag_obj)
        return post




class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write a comment...'}),
        }

