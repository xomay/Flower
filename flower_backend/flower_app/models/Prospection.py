from django.conf import settings
from django.db import models

from rest_framework import serializers

from flower_app.models.People.Membre import Membre

from datetime import date

class ContactWay(models.Model):
    contactWay = models.CharField(max_length=100)

    def __str__(self):
        return self.contactWay

    def anonymiser(self):
        self.contactWay = settings.ANONYMISATION_STRING
        self.save()

class ContactWaySerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactWay
        fields = '__all__'

class TypeAction(models.Model):
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.type

class TypeActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeAction
        fields = '__all__'

class Action(models.Model):
    type = models.ForeignKey(TypeAction, on_delete=models.RESTRICT)
    name = models.CharField(max_length=80, default="ActionCom")
    date = models.DateField(auto_now_add=False)
    comments = models.TextField(blank=True)                        #to add some stats and comments after the event
    participants = models.ManyToManyField(Membre)
    instructions = models.TextField()                              #from the responsible
    appointments = models.IntegerField(blank=True, default=0)      #to create stats to show
    studies = models.IntegerField(blank=True, default=0)           #to create stats to show

    def __str__(self):
        return self.name + str(self.type) + self.date.isoformat()

    class Meta: # Affichage custom dans l'onglet d'administration
        verbose_name = 'Action commerciale'
        verbose_name_plural = 'Actions commerciales'

class SimuAction(Action):
    class Meta:
        verbose_name = "SimuAction"
        verbose_name_plural = "SimuActions"

class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = '__all__'
