from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.core.cache import cache
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from users.forms import UserCreateForm, UserUpdateForm, CustomLoginForm
from django.contrib import messages


class RegisterView(View):
    def get(self, request):
        return render(request, "users/registration.html", {"form": UserCreateForm()})

    def post(self, request):
        form = UserCreateForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()
            login(request, user)
            messages.success(request, "Account successfully created!")
            return redirect("users:profile")

        messages.error(request, "There was an error with your registration.")
        return render(request, "users/registration.html", {"form": form})


class CustomLoginView(View):
    def get(self, request):
        return render(request, "users/login.html", {"form": CustomLoginForm()})

    def post(self, request):
        form = CustomLoginForm(data=request.POST)
        print(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                messages.success(request, "You have successfully logged in.")
                return redirect("landing_page")

        messages.error(request, "Invalid username or password.")
        return render(request, "users/login.html", {"form": form})


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "users/profile.html", {"user": request.user})

def UserLogout(request):
    logout(request)
    cache.clear()
    request.session.flush()
    messages.info(request, "You have successfully logged out.")
    return redirect("users:login")

class LogoutView(LoginRequiredMixin, View):
    def post(self, request):
        logout(request)
        cache.clear()
        request.session.flush()
        messages.info(request, "You have successfully logged out.")
        return redirect("users:login")

    def get(self, request):
        return render(request, "users/logout.html")


class ProfileUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, "users/profile_edit.html", {"form": form})

    def post(self, request):
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("users:profile")

        messages.error(request, "Error updating profile.")
        return render(request, "users/profile_edit.html", {"form": form})
