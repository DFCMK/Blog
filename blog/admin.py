from django.contrib import admin
from .models import Post
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Post)# Based on CI walk threw project
class PostAdmin(SummernoteModelAdmin):

    list_display = ('title', 'slug', 'status')
    search_fields = ['title', 'content']
    list_filter = ('status', 'date_posted')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)



# Register your models here
# admin.site.register(Post)