from django.db import models
from rest_framework import serializers

class Competence(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class CompetenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competence
        fields = '__all__'