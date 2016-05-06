from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from accounts.extra import ContentTypeRestrictedFileField


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
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_new = models.BooleanField(default=True)

    photo = models.URLField(max_length=200,blank=True,null=True)
    photo_email = ContentTypeRestrictedFileField(upload_to='Accounts/Foto',blank=True,null=True,content_types=['image/jpg', 'image/jpeg', 'image/png'],max_upload_size=1048576)
    tipo_identificacion = models.CharField(max_length=100,blank=True)
    identificacion = models.BigIntegerField(blank=True,null=True)
    fecha_nacimiento = models.DateField(blank=True,null=True)
    genero = models.CharField(max_length=100,blank=True)
    estado_civil = models.CharField(max_length=100,blank=True)
    telefono_1 = models.CharField(max_length=100, blank=True, null=True)
    telefono_2 = models.CharField(max_length=100, blank=True, null=True)
    departamento = models.CharField(max_length=100,blank=True)
    ciudad = models.CharField(max_length=100,blank=True)
    direccion = models.CharField(max_length=100,blank=True)

    titulo = models.CharField(max_length=100,blank=True)
    perfil = models.TextField(max_length=500,blank=True)

    hv = ContentTypeRestrictedFileField(upload_to='Accounts/Hv',blank=True,null=True,content_types=['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'],max_upload_size=10485760)


    def get_full_name(self):
        return self.email
    def get_short_name(self):
        return self.email

class PreUser(models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    fullname = models.CharField(max_length=100)
    code = models.CharField(max_length=255)