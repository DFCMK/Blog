from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm
from .models import Profile
from blog.models import Post
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


#tutorial based
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

# tutorial based
# Displaying user_posts based on: https://www.youtube.com/watch?v=PXqRPqDjDgc
# Pagination based on: https://docs.djangoproject.com/en/5.0/ref/paginator/#django.core.paginator.Paginator
@login_required
def profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    user_posts = Post.objects.filter(author=request.user)
    paginate_by = 6

    paginator = Paginator(user_posts, paginate_by)
    page_number = request.GET.get('page')

    try:
        user_posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        user_posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        user_posts = paginator.page(paginator.num_pages)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f"Your profile has been updated!")
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)
        
    context = {'profile': profile, 'user_form': user_form, 'profile_form': profile_form, 'user_posts':user_posts}
        
    return render(request, 'users/profile.html', context)



# Based on Stack Overflow: https://stackoverflow.com/questions/33715879/how-to-delete-user-in-django
@login_required
def delete_profile(request):
    try:
        user = request.user
        user.profile.delete()
        user.delete()           
        messages.success(request, "Your profile has been deleted successfully.")
    except User.DoesNotExist:
        messages.error(request, "The user does not exist.")
    return redirect('blog-home')
