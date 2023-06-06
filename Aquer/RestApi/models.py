from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The username field must be set.")

        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=150)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=150)
    amount_deposited = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    profile_pics = models.ImageField(upload_to="images/profile_pics", max_length=200, blank=True)
    address = models.CharField(max_length=250, blank=True)
    phone_number = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)


    USERNAME_FIELD = 'username'

    objects = UserManager()


class Category(models.Model):
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to="images/categories")



class Product(models.Model):
    name = models.CharField(max_length=250)
    price = models.FloatField()
    description = models.CharField(max_length=500)
    image = models.ImageField(upload_to="images/products", max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ["name", 'date_created']


class FundAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    date_funded = models.DateTimeField()
    status = models.CharField(max_length=150)


class ProductPayment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    fee = models.DecimalField(max_digits=6, decimal_places=2)
    payment_date = models.DateTimeField()
    status = models.CharField(max_length=150)