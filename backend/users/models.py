from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    """
    Кастомизированная модель пользователя.
    """
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    email = models.EmailField(
        verbose_name='Электронная почта',
        blank=False,
        unique=True,
        max_length=254,)

    username = models.CharField(
        verbose_name='Имя пользователя',
        unique=True,
        blank=False,
        max_length=150,
        validators=[
            RegexValidator(
                regex='^[\w.@+-]+',
                message='Неверное имя пользователя',
            ),
        ])

    first_name = models.CharField(
        verbose_name='Имя',
        blank=False,
        max_length=150,)

    last_name = models.CharField(
        verbose_name='Фамилия',
        blank=False,
        max_length=150,)

    password = models.CharField(
        verbose_name='Пароль пользователя',
        blank=False,
        max_length=150,)

    @property
    def is_admin(self):
        return self.role == self.is_staff

    class Meta:
        ordering = ['username']


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
        help_text='Содержит подписчика')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор подписки',
        help_text='Содержит автора подписки')

    def __str__(self) -> str:
        return self.author.username

    class Meta:
        ordering = ['author']
