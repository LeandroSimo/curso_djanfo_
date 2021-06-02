from re import T
from django.contrib.auth import forms
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.conf import settings
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
#from django.contrib.auth import logout

from core.utils import generate_hash_key

from .forms import RegisterForm, EditAccountForm, PasswordResetForm, User
from .models import PasswordReset

User = get_user_model()

@login_required
def dashboard(request):
    template_name = 'dashboard.html'
    return render(request, template_name)



def register(request):
    template_name = 'register.html'
    try:
        logout(request)
    except:
        pass
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        user = authenticate(username=user.username, password=form.cleaned_data['password1'])
        login(request, user)
        return redirect('core:home')
    context = {
      'form': form
    }
    return render(request, template_name, context)


def password_reset(request):
    template_name = 'password_reset.html'
    context = {}
    form = PasswordResetForm(request.POST or None)
    if form.is_valid():
        user = User.objects.get(email=form.cleaned_data['email'])
        key = generate_hash_key(user.username)
        reset = PasswordReset(key=key, user=user)
        reset.save()
        context['success'] = True
    context['form'] = form
    return render(request, template_name, context)


@login_required
def edit(request):
    template_name = 'edit.html'
    context = {}
    if request.method == 'POST':
        form = EditAccountForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            form = EditAccountForm(instance=request.user)
            context['success'] = True
           
    else:
        form = EditAccountForm(instance=request.user)
    context = {'form': form}
    return render(request, template_name, context)


@login_required
def edit_password(request):
    template_name = 'edit_password.html'
    context = {}
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            context['success'] = True
    else:
        form = PasswordChangeForm(user=request.user)
    context['form'] = form
    return render(request, template_name, context)



#def logout_view(request):
#    template_name = 'home.html'
#    logout(request)
#   return render ( request, template_name )