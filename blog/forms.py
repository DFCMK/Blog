from django import forms
from .models import Post, Comment


class CreateNewPostForm(forms.ModelForm):
    class Meta: 
        model = Post
        fields = ['title', 'slug', 'content', 'excerpt', 'featured_image']

    def save(self, commit=True):
        instance = super(CreateNewPostForm, self).save(commit=False)
        if commit:
            instance.save()
            if self.cleaned_data['featured_image']:
                instance.featured_image = self.cleaned_data['featured_image']
                instance.save()
        return instance


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'content', 'excerpt', 'featured_image']


# Based on Djangocentral: https://djangocentral.com/creating-comments-system-with-django/
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)