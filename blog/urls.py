from django.urls import path
from .views import PostListView, post_detail, create_new_post, update_post, delete_post, edit_comment, delete_comment
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('<slug:slug>/', views.post_detail, name="post_detail"),
    path('create', create_new_post, name="new_post"),
    path('update_post/<slug:slug>/', views.update_post, name='update_post'),
    path('delete_post/<slug:slug>/', views.delete_post, name='delete_post'),
    path('<slug:slug>/edit_comment/<int:comment_id>', views.edit_comment, name='edit_comment'), # CI Walk threw 
    path('<slug:slug>/delete_comment/<int:comment_id>', views.delete_comment, name='delete_comment'), # CI Walk threw
    path('about/', views.about, name='blog-about')
]