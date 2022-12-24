from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.shortcuts import render, redirect

from .forms import SignUpForm, AuthUserForm, UserProfileForm
from django.contrib.auth import login, authenticate

from .models import Profile
from .utils import send_mail_to_verify


@login_required()
def profile_view(request):
    context = {'title': 'My profile'}
    return render(request, 'auth/profile.html', context=context)


@login_required()
def profile_update(request, id):
    if request.method == "POST":
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile')
    else:
        profile_form = UserProfileForm(instance=request.user.profile)
    context = {'profile_form': profile_form, 'title': 'Update profile'}
    return render(request, 'auth/profile_update.html', context)


def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='User')
            user_to_group = User.objects.get(username=user)
            group.user_set.add(user_to_group)
            send_mail_to_verify(request, user)
            redirect('index')
        else:
            return render(request, 'auth/user_register.html', {'form': form, 'title': 'Sign up'})
    form = SignUpForm()
    return render(request, "auth/user_register.html", {"form": form, "title": "Sign up"})


def login_view(request):
    if request.method == "POST":
        form = AuthUserForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user.profile.verified and user is not None:
                login(request, user)
                messages.success(request, "<b>You are successfully logged in!</b>")
                return redirect('index')
            else:
                messages.error(request,
                               '<b>Your email has not been verified.</b> Check your email inbox and try again.')
        else:
            return render(request, 'auth/user_login.html', {'form': form, 'title': 'Sign up'})
    form = AuthUserForm()
    return render(request, 'auth/user_login.html', {'form': form, 'title': 'Sign in'})


@login_required
def logout_view(request):
    logout(request)
    return redirect('index')
