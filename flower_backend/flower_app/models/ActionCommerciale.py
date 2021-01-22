from django.db import models
from rest_framework import serializers

from flower_app.models.People.Membre import Membre, MembreSerializer
from flower_app.models.People.Prospect import Prospect, ProspectSerializer

class ActionCommerciale(models.Model):
    actionType = models.CharField(max_length=60)
    name = models.CharField(max_length=60)
    date = models.DateField(blank=True, null=True)
    prospect = models.ForeignKey(Prospect, on_delete=models.RESTRICT)
    consignes = models.TextField()
    participants = models.ManyToManyField(Membre)

    def __str__(self):
        return self.name

class ActionCommercialeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActionCommerciale
        fields = '__all__'
