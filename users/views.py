from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm
from .models import Profile
from blog.models import Post
# from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# tutorial based
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(
                request,
                f"Your account as {username} has been created!" +
                " You are now able to log in.",
            )
            return redirect("login")
        else:
            messages.error(
                request,
                "There was an error in the registration form." +
                " Please correct it.",
            )
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})


# tutorial based
# Displaying user_posts based on:
# https://www.youtube.com/watch?v=PXqRPqDjDgc
# Pagination based on:
# https://docs.djangoproject.com/en/5.0/ref/paginator/
@login_required
def profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    # Users own published Posts
    user_posts = Post.objects.filter(author=request.user).order_by(
        "-date_posted"
    )
    paginate_by = 6

    paginator = Paginator(user_posts, paginate_by)
    page_number = request.GET.get("page")

    try:
        user_posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        user_posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        user_posts = paginator.page(paginator.num_pages)

    # Users Favorite Posts
    liked_posts = Post.objects.filter(likes=request.user).order_by(
        "-date_posted"
    )
    liked_paginate_by = 6

    liked_paginator = Paginator(liked_posts, liked_paginate_by)
    liked_page_number = request.GET.get("liked_page")

    try:
        liked_posts = liked_paginator.page(liked_page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        liked_posts = liked_paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        liked_posts = liked_paginator.page(liked_paginator.num_pages)

    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            username = request.user.username
            messages.success(
                request, f"Your profile {username} has been updated!"
                )
            return redirect("profile")
        else:
            # Handle form validation errors
            for field, errors in user_form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
            for field, errors in profile_form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
            return redirect("profile")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)

    context = {
        "profile": profile,
        "user_form": user_form,
        "profile_form": profile_form,
        "user_posts": user_posts,
        "liked_posts": liked_posts,
    }

    return render(request, "users/profile.html", context)


# Based on Stack Overflow:
# https://stackoverflow.com/questions/33715879/how-to-delete-user-in-django
@login_required
def delete_profile(request):
    try:
        user = request.user
        username = user.username
        user.profile.delete()
        user.delete()
        messages.success(
            request, f"Your profile {username} has been deleted successfully."
        )
    except User.DoesNotExist:
        messages.error(request, "The user does not exist.")
    return redirect("logout")
