from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with 'email' field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email number must be set')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    # first_name, last_name already have
    image = models.ImageField(upload_to='users/', null=True, blank=True)

    is_ban = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Basket(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    furniture = models.ForeignKey('shop.Furniture', on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()


class Order(models.Model):
    STATUS = (
        ('new', 'New'),
        ('confirmed', 'Confirmed'),
        ('on_way', 'On way'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS, default=STATUS[0][0])

    phone_number = models.CharField(max_length=15)
    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email


class OrderDetail(models.Model):
    CURRENCY = (
        ('TRY', 'TRY'),
        ('USD', 'USD'),
        ('UZS', 'UZS'),
    )
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    furniture = models.ForeignKey('shop.Furniture', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=11, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY)
    quantity = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.price} {self.currency}"

    class Meta:
        unique_together = ['order', 'furniture']
