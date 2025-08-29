from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

# 1. python manage.py makemigrations
# 2. python manage.py migrate


#carreras del instituto
class Career(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

#clubes del instituto
class Clubs(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Rol(models.Model):
    id = models.BigAutoField(primary_key=True)
    rol = models.CharField(max_length=50)

    def __str__(self):
        return self.rol


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField(unique=True)
    career = models.ForeignKey(Career, on_delete=models.PROTECT, null=True, blank=True)
    clubs = models.ManyToManyField(Clubs, blank=True)
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"