from django.conf import settings
from django.db import models

from rest_framework import serializers

from flower_app.models.People.Membre import Membre
from flower_app.models.Prospection import Action, ContactWay

class Prospect(models.Model):
    name = models.CharField(max_length=60)
    address = models.CharField(max_length=200)
    address_tresorerie = models.TextField(blank=True, null=True)
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
    prospectAction = models.ManyToManyField(Action, blank=True)
    contactWay = models.ManyToManyField(ContactWay, blank=True)

    def __str__(self):
        return self.name

    def anonymiser(self):
        self.address = settings.ANONYMISATION_STRING
        self.address_tresorerie = settings.ANONYMISATION_STRING
        self.town = settings.ANONYMISATION_STRING
        self.name = settings.ANONYMISATION_STRING
        self.postcode = settings.ANONYMISATION_STRING
        for elt in self.contactWay.all():
            elt.anonymiser()
        for elt in self.employe_set.all():
            elt.anonymiser()
        self.save()

class ProspectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prospect
        fields = '__all__'
