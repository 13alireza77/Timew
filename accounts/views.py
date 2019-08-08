from django.shortcuts import render, redirect
from django.urls import reverse
from accounts.forms import (
    registrationForm,
    editProfileForm,
    UserForm,
    # password_reset
)
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash, authenticate, login
from django.contrib.auth.decorators import login_required


def view_profile(request, pk=None):
    user = request.user
    context = {
        'user': user
    }
    return render(request, 'accounts/profile.html', context)


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('accounts:view_profile')
    context = {
        "form": form,
    }
    return render(request, 'accounts/register_form.html', context)


def edit_profile(request):
    if request.method == 'POST':
        form = editProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse('accounts:view_profile'))
    else:
        form = editProfileForm(instance=request.user)
        context = {
            'form': form
        }
        return render(request, 'accounts/edit_profile.html', context)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('accounts:view_profile'))
        else:
            return redirect(reverse('accounts:change_password'))
    else:
        form = PasswordChangeForm(user=request.user)
        context = {
            'form': form
        }
        return render(request, 'accounts/change_password.html', context)
