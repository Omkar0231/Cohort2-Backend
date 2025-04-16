from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from datetime import timedelta
import random

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.is_active = True
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (
        (1, 'Male'),
        (2, 'Female'),
        (3, 'Other'),
    )

    ROLE_CHOICES = (
        ('student', 'Student'),
        ('mentor', 'Mentor'),
        ('admin', 'Admin'),
    )

    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    gender = models.SmallIntegerField(choices=GENDER_CHOICES)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    phone = models.CharField(max_length=15, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # OTP Fields
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['gender']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return True

    def generate_otp(self):
        self.otp = str(random.randint(100000, 999999))
        self.otp_created_at = timezone.now()
        self.save()

    def is_otp_valid(self, otp_input):
        if not self.otp or not self.otp_created_at:
            return False
        expiry_time = self.otp_created_at + timedelta(minutes=5)
        return self.otp == otp_input and timezone.now() <= expiry_time

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']

class EmailOTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=10)

    def __str__(self):
        return f"{self.email} - {self.otp}"
