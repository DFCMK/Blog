from django import forms
from .models import Post, Comment
from django_summernote.widgets import SummernoteWidget



class CreateNewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'category',
            #'slug',
            'content',
            'excerpt',
            'featured_image',
            'status'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'excerpt': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'content': SummernoteWidget(),
            'status': forms.Select(attrs={'class': 'form-control'}),
            }

    def __init__(self, *args, **kwargs):
        super(CreateNewPostForm, self).__init__(*args, **kwargs)
        if 'slug' in self.fields:
            del self.fields['slug']

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
        fields = [
            'title',
            'category',
            #'slug',
            'content',
            'excerpt',
            'featured_image',
            'status'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'excerpt': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'content': SummernoteWidget(),
            'status': forms.Select(attrs={'class': 'form-control'}),
            }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.update_slug()
        if commit:
            instance.save()
        return instance


# Based on Djangocentral:
# https://djangocentral.com/creating-comments-system-with-django/
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
