from django.urls import path
from .views import PostListView, post_detail, create_new_post, update_post
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('<slug:slug>/', views.post_detail, name="post_detail"),
    path('create', create_new_post, name="new_post"),
    path('update_post/<slug:slug>/', views.update_post, name='update_post'),
    path('about/', views.about, name='blog-about')
]