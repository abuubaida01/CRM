from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from django.contrib.auth.models import Group, Permission
from django.db import transaction


class User(AbstractUser):
    email = models.EmailField(('email address'), unique=True)
    # username = models.CharField(max_length=100, unique=True)
    date_of_birth = models.DateField(null=True)
    full_name = models.CharField(max_length=100)
    religion = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    email_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, related_name='users', blank=True)
    permissions = models.ManyToManyField(Permission, related_name='users', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name', 'religion', 'gender', 'date_of_birth']

    objects = UserManager()

    def __str__(self):
        return self.username 




class EmailVerificationToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='UsrVerTok')
    token = models.CharField(max_length=150)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user


# @transaction.atomic
# def delete_user_and_related_data(user_id):
#     try:
#         # Check if the user exists
#         user = User.objects.get(id=user_id)

#         # Delete related email verification tokens
#         EmailVerificationToken.objects.filter(user=user).delete()

#         # Delete the user
#         user.delete()

#         return True  # Deletion was successful
#     except User.DoesNotExist:
#         return False  # User not found


# from django.db import models
# from django.contrib.auth.models import Group, AbstractUser, BaseUserManager, Permission



# class User(AbstractUser):
#     email = models.EmailField(('email address'), unique=True)
#     date_of_birth = models.DateField(null=True)
#     full_name = models.CharField(max_length=100)
#     religion = models.CharField(max_length=100)
#     gender = models.CharField(max_length=100) 

#     is_staff = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     is_superuser = models.BooleanField(default=False)
#     groups = models.ManyToManyField(Group, related_name='users', blank=True)
#     permissions = models.ManyToManyField(Permission, related_name='users', blank=True)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username', 'full_name', 'religion', 'gender', 'date_of_birth']

#     objects = UserManager()

#     def __str__(self):
#         return self.username 