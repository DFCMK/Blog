from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm
from .models import Profile
from django.http import HttpResponseRedirect



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


#@login_required
#def delete_profile(request):
#    profile = request.user.profile
#
#    if profile.user == request.user:
#        profile.delete()
#        messages.add_message(request, messages.SUCCESS, f'{request.user.username} deleted!')
#
#    else:
#        messages.add_message(request, messages.ERROR, 'You can only delete your own Profile!')
#    
#    return HttpResponseRedirect(reverse('login'))


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

