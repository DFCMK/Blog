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


def post_detail(request, slug):
    """
    Function-based view to display a specific post based on its slug and primary key.
    """

    try:
        # Attempt to retrieve the post object based on slug and pk
        post = get_object_or_404(Post, slug=slug)
    except Post.DoesNotExist:
        # Handle the case where the post does not exist
        return render(request, '404.html', status=404)  # Render a 404 page

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



def about(request):
        return render(request, 'blog/about.html', {'title': 'About'})


