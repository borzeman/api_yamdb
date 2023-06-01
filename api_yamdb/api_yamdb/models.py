from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    password = models.CharField(blank=True, max_length=255)
    is_staff = models.BooleanField(verbose_name='Is admin?', default=False)
    is_moderator = models.BooleanField(
        verbose_name='Is moderator?',
        default=False)
    email = models.EmailField(max_length=255, primary_key=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff

    # def is_moderator():
    #     pass


class ConfirmCode(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='confirmation_code',
        primary_key=True
    )
    confirmation_code = models.CharField(blank=True, max_length=255)
