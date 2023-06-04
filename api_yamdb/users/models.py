from django.contrib.auth.models import AbstractUser
<<<<<<< HEAD
=======
from django.db.models.signals import m2m_changed, post_save
>>>>>>> auth
from django.db import models

ROLE = (
    ('User', 'User'),
    ('Moderator', 'Moderator'),
    ('Admin', 'Admin')
)

class CustomUser(AbstractUser):
<<<<<<< HEAD
    password = models.CharField(blank=True, max_length=255)
    is_staff = models.BooleanField(verbose_name='Is admin?', default=False)
    is_moderator = models.BooleanField(
        verbose_name='Is moderator?',
        default=False)
    email = models.EmailField(max_length=255, unique=True)
=======
    password = models.CharField(blank=True, max_length=254)
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
>>>>>>> auth
    bio = models.TextField(blank=True)
    role = models.CharField(max_length=255, choices=ROLE, default='User')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

<<<<<<< HEAD
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
=======
    def has_module_perms(self, app_label):
        return self.is_staff

    def has_perm(self, perm, obj=None):
        return self.is_staff

# def role_post_save(sender, instance, created, *args, **kwargs):
#     if not instance.is_staff and instance.role == 'Admin':
#         instance.is_staff = True
#         instance.save()
    
#     if instance.is_staff and instance.role != 'Admin':
#         instance.is_staff = False
#         instance.save()
        
#     if instance.is_superuser and instance.role != 'Admin':
#         instance.role = 'Admin'
#         instance.is_staff = True
#         instance.save()

    


# post_save.connect(role_post_save, sender=CustomUser)


class ConfirmCode(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='confirmation_code',
        unique=True,
    )
    confirmation_code = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.user.username
>>>>>>> auth
