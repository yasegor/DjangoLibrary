from django.contrib.auth import logout
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import login


def register_request(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'auth/user_register.html', {'form': form, 'title': 'Sign up'})
    form = SignUpForm()
    return render(request=request, template_name="auth/user_register.html", context={"form": form, "title": "Sign up"})


def logout_view(request):
    logout(request)
    return redirect('index')
