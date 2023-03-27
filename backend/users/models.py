from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='Почта',
        max_length=254,
        unique=True,
    )
    username = models.CharField(
        verbose_name='Юзернейм',
        max_length=150,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=False,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=False,
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=150,
    )
    is_subscribed = models.BooleanField(
        verbose_name='Подписка',
        default=False,
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name', 'password')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username

    @receiver(post_save, sender=AbstractUser)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        if created and instance.is_superuser:
            Token.objects.create(user=instance)
