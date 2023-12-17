from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, username, full_name, religion, gender, date_of_birth, password=None, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            full_name=full_name,
            religion=religion,
            gender=gender,
            date_of_birth=date_of_birth,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, full_name, religion, gender, date_of_birth, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, username, full_name, religion, gender, date_of_birth, password, **extra_fields)




# class UserManager(BaseUserManager):
#     def create_user(self, email, username, full_name, religion, gender, date_of_birth, password=None, **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')
#         email = self.normalize_email(email)
#         user = self.model(
#             email=email,
#             username=username,
#             full_name=full_name,
#             religion=religion,
#             gender=gender,
#             date_of_birth=date_of_birth,
#             **extra_fields
#         )
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, username, full_name, religion, gender, date_of_birth, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         extra_fields.setdefault('is_active', True)
        
#         if extra_fields.get('is_staff') is not True:
#             raise ValueError(_('Superuser must have is_staff=True.'))
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError(_('Superuser must have is_superuser=True.'))
#         return self.create_user(email, username, full_name, religion, gender, date_of_birth, password, **extra_fields)






#         # if not email:
#         #     raise ValueError('The Email must be set')
#         # email = self.normalize_email(email)
#         # user = self.model(email=email, **extra_fields)
#         # user.set_password(password)
#         # user.save(using=self._db)
#         # return user 
        

        #     def create_superuser(self, email, password, **extra_fields):
        # """
        # Create and save a SuperUser with the given email and password.
        # """
        # extra_fields.setdefault('is_staff', True)
        # extra_fields.setdefault('is_superuser', True)
        # extra_fields.setdefault('is_active', True)

        # if extra_fields.get('is_staff') is not True:
        #     raise ValueError(_('Superuser must have is_staff=True.'))
        # if extra_fields.get('is_superuser') is not True:
        #     raise ValueError(_('Superuser must have is_superuser=True.'))
        # return self.create_user(email, password, **extra_fields)