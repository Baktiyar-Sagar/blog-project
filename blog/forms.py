from django import forms 
from .models import Post, Comment

class PostForm(forms.ModelsForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'tag']

class CommentForm(forms.ModelForm):
    model = Comment
    fields = ['content']