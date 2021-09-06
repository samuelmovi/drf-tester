from django.db import models

# Create your models here.


class Thing(models.Model):

    name = models.CharField(max_length=100, null=True, blank=True)
    number = models.IntegerField(null=True, blank=True)
    decimal_number = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    timestamp = models.DateTimeField(null=True, blank=True)
