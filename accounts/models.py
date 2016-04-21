from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from mail_templated import send_mail
from Fastwork.settings.base import DEFAULT_FROM_EMAIL

class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        try:
            user = self.get(email=email)
        except:
            user = self.create(email=email, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        send_mail('email/bienvenida.tpl', {'email': email,'username':extra_fields['username']}, DEFAULT_FROM_EMAIL, [email])
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_active=True.')
        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'
    objects = UserManager()
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    fullname = models.CharField(max_length=100)
    photo = models.URLField(max_length=200)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    tipo_identificacion = models.CharField(max_length=100,blank=True)
    identificacion = models.BigIntegerField(blank=True,null=True)
    fecha_nacimiento = models.DateField(blank=True,null=True)
    genero = models.CharField(max_length=100,blank=True)
    estado_civil = models.CharField(max_length=100,blank=True)
    telefono_1 = models.IntegerField(blank=True,null=True)
    telefono_2 = models.IntegerField(blank=True,null=True)
    departamento = models.CharField(max_length=100,blank=True)
    ciudad = models.CharField(max_length=100,blank=True)
    direccion = models.CharField(max_length=100,blank=True)

    titulo = models.CharField(max_length=100,blank=True)
    perfil = models.TextField(max_length=500,blank=True)

    hv = models.FileField(upload_to='Accounts/Hv',blank=True,null=True)


    def get_full_name(self):
        return self.email
    def get_short_name(self):
        return self.email