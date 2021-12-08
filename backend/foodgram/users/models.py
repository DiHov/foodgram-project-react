from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy


class Role(models.TextChoices):
    USER = 'user', gettext_lazy('User')
    ADMIN = 'admin', gettext_lazy('Admin')


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(
        gettext_lazy('first name'),
        max_length=150,
        blank=False
    )
    last_name = models.CharField(
        gettext_lazy('last name'),
        max_length=150,
        blank=False
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.USER,
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
        'password',
    ]

    class Meta:
        verbose_name = 'Пользователь'

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == Role.ADMIN or self.is_superuser or self.is_staff
