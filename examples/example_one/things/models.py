from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class Thing(models.Model):

    name = models.CharField(max_length=100, null=True, blank=True)
    number = models.IntegerField(null=True, blank=True)
    decimal_number = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    timestamp = models.DateTimeField(null=True, blank=True)


class Property(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    creator = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
