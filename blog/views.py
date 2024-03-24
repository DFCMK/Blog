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


#def post_detail(request, slug):
#    """
#    Display an individual :model:`blog.Post`.
#
#    **Context**
#
#    ``post``
#        An instance of :model:`blog.Post`.
#
#    **Template:**
#
#    :template:`blog/post_detail.html`
#    """
#    queryset = Post.objects.filter(status=1)
#    post = get_object_or_404(queryset, slug=slug)
#    comments = post.comments.all().order_by("-date_posted")
#    comment_count = post.comments.filter(approved=True).count()
#    if request.method == "POST":
#        comment_form = CommentForm(data=request.POST)
#        if comment_form.is_valid():
#            comment = comment_form.save(commit=False)
#            comment.author = request.user
#            comment.post = post
#            comment.save()
#            messages.add_message(
#               request, messages.SUCCESS,
#                'Comment submitted and awaiting approval'
#            )
#    
#    comment_form = CommentForm()
#
#    return render(
#        request,
#        "blog/post_detail.html",
#        {
#            "post": post,
#            "comments": comments,
#            "comment_count": comment_count,
#            "comment_form": comment_form
#        },
#    )


# Based on users/views.py profile
#def create_new_post(request):
#    if request.method == 'POST':
#        form = CreateNewPostForm(request.POST, request.FILES)
#        if form.is_valid():
#            post = form.save(commit=False)
#            post.author = request.user
#            post.save()
#            return redirect('blog-home')
#    else:
#        form = CreateNewPostForm()
#    return render(request, 'blog/create.html', {'form': form})



# Based on users/profile view
#@login_required
#def create_new_post(request):
#        if request.method == 'POST':
#            post_form = CreateNewPostForm(request.POST, instance=request.user)
#            #image_form = FeaturedImageForm(request.POST, request.FILES)
#            if post_form.is_valid(): #and image_form.is_valid():
#                #post = post_form.save(commit=False)
#                author = request.user
#                post_form.save()
#                #image_form.save()
#                messages.success(request, 'Your post was successfully submitted!')
#                return redirect('blog-home')
#            else:
#                messages.error(request, 'There was an error submitting your post. Please check the form and try again.')
#        else:
#            post_form = CreateNewPostForm(instance=request.user)
#            #image_form = FeaturedImageForm(instance=Post)
#
#        context = {'post_form': post_form}
#        return render(request, 'blog/create.html', context)


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


# Refactorated create_new_post view
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
    return render(request, 'blog/update_post.html', context)

def about(request):
        return render(request, 'blog/about.html', {'title': 'About'})