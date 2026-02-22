from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment
from taggit.forms import TagWidget
from .models import Tag


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
        widgets = {
            'tags': TagWidget(),   
        }
    
    def save(self, user):
        post = super().save(commit=False)
        post.author = user
        post.save()
    
        tags_list = self.cleaned_data['tags'].split(',') 
        for tag_name in tags_list:
            post.tags.add(tag_name.strip())  
    
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
