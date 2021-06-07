from django.conf import settings
from django.db import models

from rest_framework import serializers

# Create your models here.
class Personne(models.Model):
    lastname = models.CharField(max_length=60)
    firstname = models.CharField(max_length=60)
    gender = models.CharField(max_length=60)
    mobile = models.CharField(max_length=60, blank=True, default='')
    email = models.EmailField()

    def anonymiser(self):
        self.lastname = settings.ANONYMISATION_STRING
        self.firstname = settings.ANONYMISATION_STRING
        self.gender = settings.ANONYMISATION_STRING
        self.mobile = settings.ANONYMISATION_STRING
        self.email = settings.ANONYMISATION_STRING
        self.save()

    class Meta:
        abstract = True