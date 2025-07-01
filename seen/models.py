from django.db import models
from datetime import date, datetime, timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings


User = settings.AUTH_USER_MODEL

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100,blank=True,null=True) 
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.Contact}"


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError('3e6i Email field ')
        if not phone_number:
            raise ValueError('3e6i Phone Number field')
        if not first_name or not last_name:
            raise ValueError('3e6i First name we  Last name')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            **extra_fields
        )
        user.set_password(password) if password else user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, phone_number, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser yala y3oud is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser yala y3oud is_superuser=True.')

        
        return self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            password=password,
            **extra_fields
        )



class CustomUser(AbstractBaseUser, PermissionsMixin):
    
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, unique=True)
    is_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    birth_date = models.DateField(null=True, blank=True)
    
    # def age(self):
    #     if self.birth_date:
    #         today = date.today()
    #         return today.year - self.birth_date.year - (
    #             (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
    #         )
    #     return None  

    # age.short_description = 'Age'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["phone_number", "first_name", "last_name"]
    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.phone_number}"

    def has_perm(self, perm, obj=None):
        return self.is_superuser or self.user_permissions.filter(codename=perm).exists()

    def has_perms(self, perms, obj=None):
        return all(self.has_perm(perm) for perm in perms)

    def has_module_perms(self, app_label):
        return self.is_superuser or self.user_permissions.filter(content_type__app_label=app_label).exists()