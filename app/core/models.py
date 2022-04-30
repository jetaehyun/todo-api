from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin

class UserManager(BaseUserManager): 
    '''Class to provide helper functions to create user or superuser'''                  

    def create_user(self, email, password=None, **extra_fields):       
        '''Creates and saves a new user'''           

        if not email:
            raise ValueError('Users must have an email address') # make sure there is an email

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password) # because of encryption reasons
        user.save(using=self._db) # to support different databases

        return user

    def create_superuser(self, email, password):
        '''Creates and saves a new super user'''

        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(user=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    '''Custom user model that supports using email instead of username'''
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True) # see if user is active
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'