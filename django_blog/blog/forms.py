from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment
from taggit.forms import TagWidget


# ========================
# USER REGISTER FORM
# ========================
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# ========================
# POST FORM WITH TAGS
# ========================
class PostForm(forms.ModelForm):
    tags = forms.CharField(required=False)

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']

    def save(self, commit=True, user=None):
        post = super().save(commit=False)
        if user:
            post.author = user
        if commit:
            post.save()

            # gestion des tags
            tag_names = self.cleaned_data['tags'].split(',')
            for tag_name in tag_names:
                tag_name = tag_name.strip()
                if tag_name:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    post.tags.add(tag)

        return post


# ========================
# COMMENT FORM
# ========================
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Write a comment...'
            }),
        }
