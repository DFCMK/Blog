from django.urls import path
from .views import PostListView, post_detail
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('<slug:slug>/', views.post_detail, name="post_detail"),
    path('about/', views.about, name='blog-about')
]