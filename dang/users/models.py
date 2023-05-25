from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)

        user = self.model(
            email=email,
            **extra_fields
        )

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser has to have is_staff being True")

        return self.create_user(email=email, password=password, **extra_fields)

    def create_seller(self, email, password):
        user = self.create_user(email, password)
        user.is_seller = True
        user.save()
        return user


class User(AbstractUser):
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=80, unique=True)
    password = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255, blank=True)
    is_seller = models.BooleanField(default=False)
    rating = models.IntegerField(blank=True, default=0)

    objects=CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username



