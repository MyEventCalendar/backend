from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)

from config import settings


class Event(models.Model):
    name = models.CharField('Title', max_length=200)
    description = models.TextField('Event description', max_length=400)
    start_time = models.DateTimeField('Start time')
    end_time = models.DateTimeField('End time')
    hidden = models.BooleanField('Hidden event', default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} {self.description} {self.start_time} {self.end_time} {self.hidden}"


class UserManager(BaseUserManager):

    def create_user(self, username, telegram_id, password=None):
        if username is None:
            raise TypeError('Users must have a username.')
        if telegram_id is None:
            raise TypeError('Users must have an ID.')
        user = self.model(username=username, telegram_id=telegram_id)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, telegram_id, password):
        if password is None:
            raise TypeError('Superusers must have a password.')
        user = self.create_user(username, telegram_id, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    telegram_id = models.BigIntegerField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'telegram_id' #сообщает нам, какое поле мы будем использовать для входа в систему
    REQUIRED_FIELDS = ['username']

    objects = UserManager()
