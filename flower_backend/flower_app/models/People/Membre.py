from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

from rest_framework import serializers

from flower_app.models.People.Personne import Personne
from flower_app.models.Poste import Poste, PosteSerializer

# Create your models here.
class Membre(Personne):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    promotion = models.IntegerField()
    email_junior = models.EmailField(blank=True)
    address = models.CharField(max_length=200)
    postcode = models.CharField(max_length=20)
    town = models.CharField(max_length=60)
    country = models.CharField(max_length=60)
    nationality = models.CharField(max_length=60)
    birth_date = models.DateField()
    birth_place = models.CharField(max_length=60)
    poste = models.ForeignKey(Poste, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.firstname + ' ' + self.lastname

    def anonymiser(self):
        super().anonymiser()
        self.user = None
        self.promotion = settings.ANONYMISATION_INTEGER
        self.email_junior = settings.ANONYMISATION_STRING
        self.address = settings.ANONYMISATION_STRING
        self.postcode = settings.ANONYMISATION_STRING
        self.town = settings.ANONYMISATION_STRING
        self.country = settings.ANONYMISATION_STRING
        self.nationality = settings.ANONYMISATION_STRING
        self.birth_place = settings.ANONYMISATION_STRING
        self.birth_date = settings.ANONYMISATION_DATE
        self.save()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', )

class MembreSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    poste = PosteSerializer(read_only=True)
    class Meta:
        model = Membre
        fields = '__all__'

