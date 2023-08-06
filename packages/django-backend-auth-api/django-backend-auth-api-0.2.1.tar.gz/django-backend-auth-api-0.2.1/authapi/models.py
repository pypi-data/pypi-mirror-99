# encoding: utf-8

from __future__ import unicode_literals

from django.utils.translation import ugettext as _

from django.db import models

# Create your models here.

from django.contrib.auth.models import (
        AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
import jwt

from datetime import date, datetime, timedelta
from django.utils.timezone import now    

from django.conf import settings

from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE_CASCADE
from django.urls import reverse
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

# tags
from taggit.managers import TaggableManager
import uuid
import random,string
ADMIN = 'admin'
STANDARD = 'standard'
LIVREUR = 'livreur'
USAGER = 'usager'
VENDEUR = 'vendeur'
USER_TYPES = (
    (ADMIN, ADMIN),
    (STANDARD, STANDARD),
    (LIVREUR, LIVREUR),
    (USAGER, USAGER),
    (VENDEUR, VENDEUR)    
)

HOMME = 'homme'
FEMME = 'femme'
USER_SEXE = (
    (HOMME, HOMME),
    (FEMME, FEMME)
)

N =7
# def get_code():
#     return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin, SafeDeleteModel):
    email = models.EmailField(unique=True)
    first_name = models.CharField(_('first name'), max_length=1000, blank=False)
    last_name = models.CharField(_('last name'), max_length=1000, blank=False)
    phone = models.CharField(_('phone number'), max_length=1000, blank=True, null=True)
    date_naissance = models.DateField(_('date de naissance'),blank=True,null=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(default=False)
    avatar = models.ImageField(default="avatars/default.png", upload_to='avatars/', null=True, blank=True, max_length=1000)
    password_reset_count = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True, default=0)
    adresse = models.CharField(_('adress'), max_length=30, blank=True)
    sexe = models.CharField(max_length=20, choices=USER_SEXE, blank=True, default=HOMME)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, blank=True, default=USAGER)
    age = models.PositiveIntegerField(default=18)
    first_connexion = models.BooleanField(default=True, null=True)
    region=models.CharField(_('region'), max_length=300, blank=True,null=True)
    ville=models.CharField(_('ville'), max_length=300, blank=True,null=True)

    
    objects = UserManager()

    
    USERNAME_FIELD = 'email'
    # these field are required on registering
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
    def __str__(self):
        return str(self.email) + ''
    
    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

class PasswordReset(models.Model):
    code = models.CharField(max_length=7, blank=False, null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=False, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)
    date_used = models.DateTimeField(null=True)
