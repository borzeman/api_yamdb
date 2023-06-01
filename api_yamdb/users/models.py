from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE = (
    ('User', 'User'),
    ('Moderator', 'Moderator'),
    ('Admin', 'Admin')
)

class CustomUser(AbstractUser):
    password = models.CharField(blank=True, max_length=255)
    is_staff = models.BooleanField(verbose_name='Is admin?', default=False)
    is_moderator = models.BooleanField(
        verbose_name='Is moderator?',
        default=False)
    email = models.EmailField(max_length=255, unique=True)
    bio = models.TextField(blank=True)
    role = models.CharField(max_length=255, choices=ROLE, default='User')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    # def has_perm(self, perm, obj=None):
    #     return self.is_staff

    # def has_module_perms(self, app_label):
    #     return self.is_staff


class ConfirmCode(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='confirmation_code',
    )
    confirmation_code = models.CharField(blank=True, max_length=255)
