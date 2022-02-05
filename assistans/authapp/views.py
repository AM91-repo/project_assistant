from django.contrib import auth
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from authapp.forms import UserLoginForm, UserCreationForm, UserChangeForm, UserProfileChangeForm
from authapp.models import User, UserProfile


def login(request):
    redirect_to = request.GET.get('next', '')

    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            redirect_to = request.POST.get('redirect-to')
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(redirect_to or reverse('base:index'))
    else:
        form = UserLoginForm()

    context = {
        'page_title': 'логин',
        'form': form,
        'redirect_to': redirect_to,
    }
    return render(request, 'authapp/login.html', context)


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('base:index'))


def register(request):
    if request.method == 'POST':
        register_form = UserCreationForm(request.POST, request.FILES)
        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.is_active = False
            user.set_activation_code()
            user.save()
            if not user.send_email_for_confirmation():
                return HttpResponseRedirect(reverse('auth:register'))
            return HttpResponseRedirect(reverse('base:index'))
    else:
        register_form = UserCreationForm()

    context = {
        'page_title': 'регистрация',
        'form': register_form,
    }
    return render(request, 'authapp/register.html', context)


@login_required
def edit(request):
    if request.method == 'POST':
        form = UserChangeForm(
            request.POST, request.FILES, instance=request.user)
        profile_form = UserProfileChangeForm(request.POST, request.FILES,
                                             instance=request.user.userprofile)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('base:index'))
    else:
        form = UserChangeForm(instance=request.user)
        profile_form = UserProfileChangeForm(
            instance=request.user.userprofile)

    context = {
        'page_title': 'редактирование',
        'form': form,
        'profile_form': profile_form,
    }
    return render(request, 'authapp/update.html', context)


def verify(request, email, activate_code):
    user = get_user_model().objects.filter(email=email).first()
    if user.activate_code == activate_code and not user.is_activation_key_expired:
        user.is_active = True
        user.save()
        auth.login(request, user,
                   backend='django.contrib.auth.backends.ModelBackend')
    return render(request, 'authapp/verification.html')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
