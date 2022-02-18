from curses.ascii import US
from django.db.models import Q
from multiprocessing import context
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DeleteView, CreateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test

from authapp.forms import UserLoginForm, UserCreationForm, UserChangeForm, UserProfileChangeForm, FriendRequestCreateForm
from authapp.models import User, UserProfile, FriendRequest


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
        register_form = UserCreationForm(request.POST)
        # register_form = UserCreationForm(request.POST, request.FILES)
        if register_form.is_valid():
            # user = register_form.save(commit=False)
            # user.is_active = False
            # user.set_activation_code()
            register_form.save()
            # if not user.send_email_for_confirmation():
            #     return HttpResponseRedirect(reverse('auth:register'))
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


@login_required
def list_friends(request):
    user = request.user
    # friends = FriendRequest.objects.filter(
    #     from_user=user, to_user=user, accepte=True).all()
    # friends_user = friends.select_related('from_user').select_related(
    #     'to_user').exclude(from_user=user, to_user=user)

    friends = user.friends.all()

    context = {
        'friends': friends
    }
    return render(request, 'authapp/friends_list.html', context)


@login_required
def friend_request(request):
    text_error = ''
    if request.method == 'POST':
        name_user = request.POST.get('name')
        user = request.user
        print(f'form: {name_user}')

        friend = user.friends.all()

        requested_user = User.objects.filter(username=name_user).first()
        requests_exist = FriendRequest.objects.filter(
            from_user=user, to_user=requested_user).first()

        if requested_user and not friend and not requests_exist:

            friends = FriendRequest.objects.filter(
                from_user=user, to_user=user, accepte=True).select_related(
                'from_user').select_related(
                'to_user').exclude(from_user=user, to_user=user)

            create_request = FriendRequest()
            create_request.from_user = user
            create_request.to_user = requested_user
            create_request.save()
            return HttpResponseRedirect(reverse('authapp:friends'))
        text_error = 'Такого пользователя нет. Попробуйте еще'

    context = {
        'page_title': 'запрос',
        'text_error': text_error,
    }
    return render(request, 'authapp/friendrequest_form.html', context)
    # return HttpResponseRedirect(reverse('authapp:friends'))


@login_required
def accept_friend_request(request, pk):
    friend_request = FriendRequest.objects.get(id=pk)
    friend_request.to_user.friends.add(friend_request.from_user)
    friend_request.from_user.friends.add(friend_request.to_user)
    friend_request.is_active = False
    friend_request.accepte = True
    friend_request.save()
    return HttpResponseRedirect(reverse('auth:request'))


class UserIsAuthMixin:
    @method_decorator(user_passes_test(lambda user: user.is_authenticated))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class PageTitleMixin:
    page_title_key = 'page_title'
    page_title = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.page_title_key] = self.page_title
        return context


class FriendRequestList(UserIsAuthMixin, PageTitleMixin, ListView):
    model = FriendRequest
    page_title = 'пользователь/запросы'

    def get_queryset(self):
        friends = FriendRequest.objects.filter(
            Q(from_user=self.request.user) |
            Q(to_user=self.request.user)).filter(is_active=True).all()
        return friends


class FriendRequestDelete(UserIsAuthMixin, PageTitleMixin, DeleteView):
    model = FriendRequest
    success_url = reverse_lazy('auth:request')
    page_title = 'пользователь/запросы/удаление'


# def friend_budget

# class FriendRequestCreate(UserIsAuthMixin, PageTitleMixin, CreateView):
#     model = FriendRequest
#     form_class = FriendRequestCreateForm
#     success_url = reverse_lazy('auth:friends')
#     page_title = 'пользователь/запрос'

#     def form_valid(self, form):
#         obj = form.save(commit=False)
#         obj.from_user = self.request.user
#         return super(FriendRequest, self).form_valid(form)


# class FriendList(UserIsAuthMixin, PageTitleMixin, ListView):
#     model = FriendRequest
#     page_title = 'пользователь/запрос'


# def verify(request, email, activate_code):
#     user = get_user_model().objects.filter(email=email).first()
#     if user.activate_code == activate_code and not user.is_activation_key_expired:
#         user.is_active = True
#         user.save()
#         auth.login(request, user,
#                    backend='django.contrib.auth.backends.ModelBackend')
#     return render(request, 'authapp/verification.html')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
