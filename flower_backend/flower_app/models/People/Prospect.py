from django.db import models

from rest_framework import serializers
from flower_app.models.People.Membre import Membre
from flower_app.models.Prospection import Action, ContactWay

class Prospect(models.Model):
    name = models.CharField(max_length=60)
    address = models.CharField(max_length=200)
    postcode = models.CharField(max_length=20)
    town = models.CharField(max_length=60)
    charge = models.ForeignKey(Membre, blank=True, null=True, on_delete=models.SET_NULL)
    AV_LEVELS = [
        ('NC','Nouveau Prospect'),
        ('AR', 'A relancer'),
        ('RDV', 'Rendez-vous obtenu'),
        ('DS', 'Devis Signé')
    ]
    advancement = models.CharField(max_length=3, choices=AV_LEVELS, default='NC')
    nextDate = models.DateField(blank=True, null = True)
    prospectAction = models.ManyToManyField(Action)
    contactWay = models.ManyToManyField(ContactWay)


    def __str__(self):
        return self.name

class ProspectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prospect
        fields = '__all__'
