from django.contrib import admin
from .models import Post, Comment
from django_summernote.admin import SummernoteModelAdmin


# Based on CI walk threw project
@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):

    list_display = ('title', 'slug', 'status')
    search_fields = ['title', 'content']
    list_filter = ('status', 'date_posted')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'body', 'date_posted', 'approved')
    list_filter = ('approved',)


# Based on Tutorial: Custom Login Page Template / Part 6
# class BlogAdminArea(admin.AdminSite):
#    site_header = 'Blog Admin Area'
#    admin_login_template = 'admin/admin_login.html'
#
# blog_admin_site = BlogAdminArea(name="BlogAdmin")


# admin.site.register(Post)
admin.site.register(Comment, CommentAdmin)
# blog_admin_site.register(Comment, CommentAdmin)
