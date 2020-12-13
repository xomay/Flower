from django.db import models
from datetime import date
from rest_framework import serializers

from flower_app.models.People.Membre import Membre


class ContactWay(models.Model):
    contactWay = models.CharField(max_length=100)

    def __str__(self):
        return self.contactWay

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
    date = models.DateField(auto_now_add=True)
    comments = models.CharField(max_length=10000)       #to add some stats and comments after the event
    participants = models.ManyToManyField(Membre)
    instructions = models.CharField(max_length=10000)   #from the responsible
    appointments = models.IntegerField(blank=True)      #to create stats to show
    studies = models.IntegerField(blank=True)           #to create stats to show

    def __str__(self):
        return self.type + self.date.isoformat()

class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = '__all__'
