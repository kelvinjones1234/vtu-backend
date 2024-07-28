from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
  email = models.EmailField(unique=True)
  phone_number = models.CharField(max_length=11, unique=True) 
  transaction_pin = models.CharField(max_length=4)
  is_premium = models.BooleanField(default=False)
  date_joined = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.username

class Wallet(models.Model):
  wallet_name = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
  balance = models.PositiveBigIntegerField(default=0)
  last_funded = models.DateTimeField(auto_now_add=True) 

  def __str__(self):
    return self.wallet_name.username


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message[:20] 