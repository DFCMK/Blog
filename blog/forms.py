from django import forms
from .models import Post

class CreateNewPostForm(forms.ModelForm):
    class Meta: 
        model = Post
        fields = ['title', 'slug', 'content', 'excerpt']