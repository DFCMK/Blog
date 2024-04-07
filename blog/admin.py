from django.contrib import admin
from .models import Post, Comment
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Post)# Based on CI walk threw project
class PostAdmin(SummernoteModelAdmin):

    list_display = ('title', 'slug', 'status')
    search_fields = ['title', 'content']
    list_filter = ('status', 'date_posted')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'body', 'date_posted', 'approved')
    list_filter = ('approved',)


# admin.site.register(Post)
admin.site.register(Comment, CommentAdmin)