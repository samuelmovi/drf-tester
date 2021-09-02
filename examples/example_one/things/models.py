from django.db import models

# Create your models here.

class Thing(models.Model):

    name = models.CharField(max_length=100, null=True, blank=True)

