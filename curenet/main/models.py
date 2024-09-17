from django.db import models
from django.contrib.auth.models import AbstractUser,  BaseUserManager, PermissionsMixin, AbstractBaseUser
from django.db.models.base import Model
from django.db.models.fields import CharField, DateField
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    phone = models.CharField(max_length=15, blank=True, null=True)
    dob = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class Doctor(models.Model):
    SPECIALITY_CHOICES = (
        ("Cardiology", "cardiology"),
        ("Dermatology", "dermatology"),
        ("Neurology", "neurology"),
        ("Pediatrician", "pediatrician"),
        ("Psychiatry", "psychiatry"),
        ("Orthopedics", "orthopedics"),
        ("Gynecology", "gynecology "),
        ("Urology", "urology"),
        ("Oncology", "oncology")
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    profile_image = models.URLField(max_length=200, null=True)
    designation = models.CharField(max_length=10, null=True)
    speciality = models.CharField(
        choices=SPECIALITY_CHOICES, max_length=20, null=True)
    experience = models.CharField(max_length=10, null=True)
    info = models.CharField(max_length=256, null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    fee = models.IntegerField(null=True)

    def __str__(self):
        return str(self.user)


class Appointment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField(null=True)
    status = models.CharField(max_length=10, default='Pending', null=True)

    def __str__(self):
        return f"{self.user} with Dr.{self.doctor.user}"


class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    review = models.CharField(max_length=256, null=True)

    def __str__(self):
        return f"{self.user}:{self.doctor.user}"
