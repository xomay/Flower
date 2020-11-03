from django.db import models

from rest_framework import serializers

class Prospect(models.Model):
    name = models.CharField(max_length=60)
    address = models.CharField(max_length=200)
    postcode = models.CharField(max_length=20)
    town = models.CharField(max_length=60)    

    def __str__(self):
        return self.name

class ProspectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prospect
        fields = '__all__'
