# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm, LoginForm
from django.views.decorators.cache import never_cache

def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            if user is not None:
                print("User authenticated")
                login(request, user)
                return redirect("home")
            else:
                print("Authentication failed")
        else:
            print("Form is invalid:", form.errors)
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {"form": form})

@never_cache
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            print("Login form is valid")
            user = form.get_user()
            login(request, user)
            return redirect("home")
        else:
            print("Login form is invalid:", form.errors)
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")
