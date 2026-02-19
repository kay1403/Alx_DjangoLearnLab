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
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'tags': TagWidget(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True, user=None):
        post = super().save(commit=False)
        if user:
            post.author = user
        if commit:
            post.save()
            self.save_m2m()  # Nécessaire pour enregistrer les tags correctement
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
