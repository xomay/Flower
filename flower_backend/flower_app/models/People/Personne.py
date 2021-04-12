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
        self.lastname = 'xxxxx'
        self.firstname = 'xxxxx'
        self.gender = 'xxxxx'
        self.mobile = 'xxxxx'
        self.email = 'xxxxx'
        self.save()

    class Meta:
        abstract = True