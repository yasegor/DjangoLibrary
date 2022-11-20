from django.contrib.auth import logout
from django.shortcuts import render, redirect
from .forms import SignUpForm, AuthUserForm
from django.contrib.auth import login, authenticate


def register_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
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
            if user is not None:
                login(request, user)
                return redirect('index')
        else:
            return render(request, 'auth/user_login.html', {'form': form, 'title': 'Sign up'})
    form = AuthUserForm()
    return render(request, 'auth/user_login.html', {'form': form, 'title': 'Sign in'})


def logout_view(request):
    logout(request)
    return redirect('index')
