from email import message
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    age = models.PositiveIntegerField('возраст', blank=True, null=True)
    # avatar = models.ImageField(upload_to='avatars', blank=True)
    # activate_code = models.CharField(max_length=128, blank=True)
    registration_start_time = models.DateTimeField(
        auto_now_add=True, null=True)
    # friends = models.ManyToManyField('User', blank=True)


class UserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = (
        (MALE, 'мужской'),
        (FEMALE, 'женский'),
    )

    user = models.OneToOneField(
        User, primary_key=True, on_delete=models.CASCADE)
    tagline = models.CharField(verbose_name='теги',
                               max_length=128, blank=True)
    about_me = models.TextField(verbose_name='о себе', blank=True)
    gender = models.CharField(verbose_name='пол', max_length=1,
                              choices=GENDER_CHOICES, blank=True)


class FriendRequest(models.Model):
    from_user = models.ForeignKey(
        User, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(
        User, related_name='to_user', on_delete=models.CASCADE)
    message_request = models.TextField(verbose_name='сообщение', blank=True)
    is_active = models.BooleanField(default=True)
    date_request = models.DateTimeField(auto_now_add=True, editable=False)
    accepte = models.BooleanField(default=False)
