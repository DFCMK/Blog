from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from cloudinary.models import CloudinaryField


# likes Based on: https://www.youtube.com/watch?v=PXqRPqDjDgc
# Down and Up vote (thumbs up/ thumbs down) based on:
# https://www.youtube.com/watch?v=onZ69P9wS2o
# Based on CI walk threw
STATUS = ((0, "Draft"), (1, "Published"))


class Post(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    featured_image = CloudinaryField(
        'post_image', default='placeholder', transformation=[{
            'width': 200,
            'height': 150,
            'crop': "fill",
            'effect': "sharpen:200"
            },
        ])
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS, default=0)
    excerpt = models.TextField(blank=True)
    likes = models.ManyToManyField(User, related_name='blog_post', blank=True)
    thumbsup = models.IntegerField(default=0)
    thumbsdown = models.IntegerField(default=0)
    thumbs = models.ManyToManyField(
        User, related_name='thumbs', default=None, blank=True
        )

    def save(self, *args, **kwargs):
        if not self.slug or self.title_changed():
            self.slug = self.generate_slug()
        super().save(*args, **kwargs)

    def title_changed(self):
        if self.pk:
            old_post = Post.objects.get(pk=self.pk)
            return self.title != old_post.title
        return False

    def generate_slug(self):
        return slugify(self.title)

    def update_slug(self):
        """
        Updates the slug based on the current title.
        """
        self.slug = self.generate_slug()
        self.save(update_fields=['slug'])

    def total_likes(self):
        return self.likes.count()

# Based on: https://www.youtube.com/watch?v=onZ69P9wS2o
class Vote(models.Model):
    post = models.ForeignKey(
        Post, related_name='postid',
        on_delete=models.CASCADE,
        default=None, blank=True
        )
    user = models.ForeignKey(
        User, related_name='userid',
        on_delete=models.CASCADE,
        default=None,
        blank=True
        )
    vote = models.BooleanField(default=True)


# Based on Post model
class Comment(models.Model):
    post = models.ForeignKey(
        'Post',
        related_name='comments',
        on_delete=models.CASCADE
        )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='commenter'
        )
    body = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    approved = models.BooleanField(default=False)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment {self.body} by {self.author}"

    class Meta:
        ordering = ["-date_posted"]