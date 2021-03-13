from django.db import models
from rest_framework import serializers

class Poste(models.Model):
    name = models.CharField(max_length=60)
    name_feminine = models.CharField(max_length=60, blank=True)
    subordinates = models.ManyToManyField("Poste", blank=True)

    def __str__(self):
        return self.name + "( -> " + str(len(self.subordinates.all())) + " )"

class PosteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poste
        fields = '__all__'
