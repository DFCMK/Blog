from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Post


def home(request):
    context = { 'posts': Post.objects.all() }
    return render(request, 'blog/home.html', context)

# Tutorial video 10 - 9:00min.
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']


# Tutorial video 10 - 11:20min
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        if slug is not None:
            return get_object_or_404(Post, slug=slug)
        return super().get_object(queryset=queryset)



def about(request):
        return render(request, 'blog/about.html', {'title': 'About'})


