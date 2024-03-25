from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from .forms import CreateNewPostForm, PostUpdateForm
from django.contrib import messages
from .models import Post

#Tutorial based
def home(request):
    context = { 'posts': Post.objects.all() }
    return render(request, 'blog/home.html', context)

# Tutorial video 10 - 9:00min.
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 6


# Based on simple.rocks: https://simpleit.rocks/python/django/generating-slugs-automatically-in-django-easy-solid-approaches/
def post_detail(request, slug):
    """
    Function-based view to display a specific post based on its slug and primary key.
    """

    try:
        post = get_object_or_404(Post, slug=slug)
       # post.generate_excerpt()
    except Post.DoesNotExist:
        return render(request, '404.html', status=404)

    context = {
        'post': post,
        'slug': slug,
    }

    return render(request, 'blog/post_detail.html', context)


# Based users/views.py profile
@login_required
def create_new_post(request):
    if request.method == 'POST':
        post_form = CreateNewPostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=True)
            messages.success(request, 'Your post was successfully submitted!')
            return redirect('blog-home')
        else:
            messages.error(request, 'There was an error submitting your post. Please check the form and try again.')
    else:
        post_form = CreateNewPostForm()
    
    context = {'post_form': post_form}
    return render(request, 'blog/create.html', context)


# Based on create_new_post view
@login_required
def update_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.user != post.author:
        messages.error(request, 'You are not authorized to edit this post.')
        return redirect('post-detail', slug=slug)

    if request.method == 'POST':
        post_form = PostUpdateForm(request.POST, request.FILES, instance=post)
        if post_form.is_valid():
            post_form.save()
            messages.success(request, 'Post updated successfully.')
            return redirect('post_detail', slug=slug)
        else:
            messages.error(request, 'There was an error updating your post. Please check the form and try again.')
    else:
        post_form = PostUpdateForm(instance=post)
    
    context = {'post_form': post_form, 'slug':slug}
    return redirect('blog-home')


# Based on update_post view
@login_required
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.user != post.author:
        messages.error(request, 'You are not authorized to delete this post!')
    else:
        post.delete()
        messages.success(request, 'Post deleted successfully!')

    return redirect('blog-home')






def about(request):
        return render(request, 'blog/about.html', {'title': 'About'})