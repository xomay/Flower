from django.conf import settings
from django.db import models

from rest_framework import serializers

from flower_app.models.People.Membre import Membre
from flower_app.models.Prospection import Action, ContactWay

class Prospect(models.Model):
    name = models.CharField(max_length=60)
    address = models.CharField(max_length=200, blank=True, null=True)
    address_tresorerie = models.TextField(blank=True, null=True)
    postcode = models.CharField(max_length=20, blank=True, null=True)
    town = models.CharField(max_length=60, blank=True, null=True)
    type = models.CharField(max_length=60, blank=True, null=True)
    domain = models.CharField(max_length=60, blank=True, null=True)
    charge = models.ForeignKey(Membre, blank=True, null=True, on_delete=models.SET_NULL)
    AV_LEVELS = [
        ('NC','Nouveau Prospect'),
        ('AR', 'A relancer'),
        ('PC', 'Devis à envoyer'),
        ('WIN', 'Prospect gagné'),
        ('LO', 'Prospect perdu')
    ]
    advancement = models.CharField(max_length=3, choices=AV_LEVELS, default='NC')
    nextDate = models.DateField(blank=True, null = True)
    prospectAction = models.ManyToManyField(Action, blank=True)
    contactWay = models.ManyToManyField(ContactWay, blank=True)

    def __str__(self):
        return self.name
    
    @property
    def addresse_facturation(self):
        if self.address_tresorerie == None or self.address_tresorerie == "":
            return self.address + ", " + str(self.postcode) + " " + self.town
        return self.address_tresorerie

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
