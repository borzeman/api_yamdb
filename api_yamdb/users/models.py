from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'
ROLE = (
    ('user', USER),
    ('moderator', MODERATOR),
    ('admin', ADMIN)
)


class CustomUser(AbstractUser):
    password = models.CharField(blank=True, max_length=254)
    email = models.EmailField(max_length=254, unique=True)
    bio = models.TextField(blank=True)
    role = models.CharField(max_length=255, choices=ROLE, default='user')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def is_admin(self):
        if self.role == 'admin' or self.is_superuser:
            return True
        return False

    def is_moderator(self):
        if self.role == 'moderator':
            return True
        return False

    def clean(self):
        super().clean()
        if self.username.upper() != self.username:
            raise ValidationError("Нет верхнему регистру!")
        if self.username.lower() == 'me':
            raise ValidationError("username != 'me'", code=400)


class ConfirmCode(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='confirmation_code'
    )
    confirmation_code = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.user.username
