from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.core.validators import MinValueValidator,MaxValueValidator
from django.contrib.auth.base_user import BaseUserManager
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.db.models.signals import post_save
import re


class CustomUserManager(BaseUserManager):
  def create_user(self,email,password=None,**extra_fields):
    if not email:
      raise ValueError("Email is required")
    match = re.match(r'\w+@\w+[.]\w+',email)
    if not match:
      raise ValueError("Email not valid")
    if not password:
      raise ValueError("Password is required")
    if len(password) < 8:
      raise ValueError("Password must be at least 8 characters")
    if any(x.isupper() for x in password) and any(x.islower() for x in password):
      email = self.normalize_email(email)
      user = self.model(email=email,**extra_fields)
      user.set_password(password)
      user.save()
      return user
    else:
      raise ValueError("Password must contain at least 1 uppercase and 1 lowercase letter")

  def create_superuser(self,email,password=None,**extra_fields):
    user = self.create_user(email=self.normalize_email(email),password=password,**extra_fields)
    user.is_staff = True
    user.is_admin = True
    user.is_superuser = True
    user.save()
    return user

class CustomUser(AbstractBaseUser,PermissionsMixin):
  email = models.EmailField(unique=True)
  full_name = models.TextField(default="full_name")
  phone = models.IntegerField(validators=[MinValueValidator(1111111111),MaxValueValidator(9999999999)])
  address = models.TextField(blank=True,null=True)
  city = models.CharField(blank=True,null=True,max_length=50)
  state = models.CharField(blank=True,null=True,max_length=50)
  country = models.CharField(blank=True,null=True,max_length=50)
  pincode = models.IntegerField(validators=[MinValueValidator(111111),MaxValueValidator(999999)])
  is_staff = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)
  is_admin = models.BooleanField(default=False)
  date_joined = models.DateTimeField(auto_now_add=True)
  is_superuser = models.BooleanField(default=False)

  objects = CustomUserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['full_name','phone','pincode']

  def __str__(self):
    return self.full_name

  
@receiver(post_save, sender=CustomUser)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)