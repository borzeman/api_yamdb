from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin')
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


class ConfirmCode(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='confirmation_code'
    )
    confirmation_code = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.user.username
