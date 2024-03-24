from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm
from .models import Profile
from django.http import HttpResponseRedirect


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
@login_required
def profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)
    
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
        
    context = {'profile': profile, 'user_form': user_form, 'profile_form': profile_form}
        
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
