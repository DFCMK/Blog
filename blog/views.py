from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.urls import reverse
from django.views.generic import ListView
from .forms import CreateNewPostForm, PostUpdateForm, CommentForm
from django.contrib import messages
from .models import Post, Comment, Vote

from django.http import JsonResponse
from django.db.models import F

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


# Create Slugs based on simple.rocks: https://simpleit.rocks/python/django/generating-slugs-automatically-in-django-easy-solid-approaches/
# Implementing comments based on djangocentral: https://djangocentral.com/creating-comments-system-with-django/ for implementing comments
# Total Likes based on: https://www.youtube.com/watch?v=PXqRPqDjDgc
# Based on CI Django Walkthrew post_detail view:
def post_detail(request, slug):
    """
    Display an individual :model:`blog.Post`.
        
    **Context**
        
    ``post``
    An instance of :model:`blog.Post`.
        
    **Template:**
        
    :template:`blog/post_detail.html`
    """

    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.all().order_by("-date_posted")
    comment_count = post.comments.filter(approved=True).count()
    total_likes_count = post.total_likes()
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Comment submitted and awaiting approval'
            )
    
    comment_form = CommentForm()

    return render(
        request,
        "blog/post_detail.html",
        {
            "post": post,
            "comments": comments,
            "comment_count": comment_count,
            "total_likes_count": total_likes_count,
            "comment_form": comment_form
        },
    )


# Based users/views.py profile
@login_required
def create_new_post(request):
    if request.method == 'POST':
        post_form = CreateNewPostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()
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
            post = post_form.save()
            post.update_slug()  # Update slug after saving the form
            post_form.save()  # Save the updated slug
            messages.success(request, 'Post updated successfully.')
            return redirect('post_detail', slug=post.slug) 
        else:
            messages.error(request, 'There was an error updating your post. Please check the form and try again.')
    else:
        post_form = PostUpdateForm(instance=post)
    
    context = {'post_form': post_form, 'slug':slug}
    return render(request, 'blog/update_post.html', context)

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

# Based on CI walk threw
@login_required
def edit_comment(request, comment_id, slug):
    post = get_object_or_404(Post, slug=slug)
    #comment_form = CommentForm(data=request.POST, instance=comment)
    comments = get_object_or_404(Comment, pk=comment_id)
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.approved = False
            comment.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Comment Updated!')
    else:
        messages.add_message(request, messages.ERROR, 'Error updating comment')

    return HttpResponseRedirect(reverse('post_detail', args=[slug]))


# Based on CI walk threw
def delete_comment(request, slug, comment_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, slug=slug)
        comment = get_object_or_404(Comment, pk=comment_id)
        if request.user == comment.author:
            comment.delete()
            messages.success(request, 'Comment deleted successfully!')
        else:
            messages.error(request, 'You can only delete your own comments!')
    else: 
        messages.error(request, 'Invalid request method!')

    return HttpResponseRedirect(reverse('post_detail', args=[slug]))


# Based on tutorial: https://www.youtube.com/watch?v=PXqRPqDjDgc
def likes(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.likes.add(request.user)
    return redirect('blog-home')

# Based on tutorial: https://www.youtube.com/watch?v=onZ69P9wS2o
def thumbs(request, pk):
    if request.method == 'POST':
        if request.POST.get('action') == 'thumbs':
            id = pk
            button = request.POST.get('button')
            update = get_object_or_404(Post, pk=id)

            # Check if user already voted
            user_vote = Vote.objects.filter(post_id=id, user_id=request.user.id).first()

            if not user_vote:  
                # User hasn't voted before
                if button == 'thumbsup':
                    update.thumbsup = F('thumbsup') + 1
                    new_vote = Vote(post_id=id, user_id=request.user.id, vote=True)
                    new_vote.save()
                else:
                    update.thumbsdown = F('thumbsdown') + 1
                    new_vote = Vote(post_id=id, user_id=request.user.id, vote=False)
                    new_vote.save()
            else:  # User has already voted
                if button == 'thumbsup' and user_vote.vote:
                    # Upvoted and clicks upvote again --> remove vote
                    update.thumbsup = F('thumbsup') - 1
                    user_vote.delete()
                elif button == 'thumbsdown' and not user_vote.vote:
                    # Downvoted and clicks downvote again --> remove vote
                    update.thumbsdown = F('thumbsdown') - 1
                    user_vote.delete()
                else:
                    # User voted with a different value before --> change vote
                    user_vote.vote = not user_vote.vote  # Flip the vote value
                    user_vote.save(update_fields=['vote'])
                    if user_vote.vote:
                        update.thumbsup = F('thumbsup') + 1
                        update.thumbsdown = F('thumbsdown') - 1
                    else:
                        update.thumbsup = F('thumbsup') - 1
                        update.thumbsdown = F('thumbsdown') + 1

            update.save()
            update.refresh_from_db()
            up = update.thumbsup
            down = update.thumbsdown
            return JsonResponse({'up': up, 'down': down})

    return JsonResponse({'error': 'Invalid request'})



def about(request):
        return render(request, 'blog/about.html', {'title': 'About'})