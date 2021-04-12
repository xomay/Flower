from django.db import models
from django.contrib.auth.models import User

from rest_framework import serializers

from flower_app.models.People.Personne import Personne

# Create your models here.
class Membre(Personne):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    promotion = models.IntegerField()
    email_junior = models.EmailField(blank=True)
    address = models.CharField(max_length=200)
    postcode = models.CharField(max_length=20)
    town = models.CharField(max_length=60)
    country = models.CharField(max_length=60)
    nationality = models.CharField(max_length=60)
    birth_date = models.DateField()
    birth_place = models.CharField(max_length=60)

    def __str__(self):
        return self.firstname + ' ' + self.lastname

    def anonymiser(self):
        super.anonymiser(self):
        self.user = 'xxxxx'
        self.promotion = 'xxxxx'
        self.email_junior = 'xxxxx'
        self.address = 'xxxxx'
        self.postcode = 'xxxxx'
        self.town = 'xxxxx'
        self.country = 'xxxxx'
        self.nationality = 'xxxxx'
        self.birth_place = 'xxxxx'
        self.birth_date = 'xxxxx'
        self.save()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', )

class MembreSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Membre
        fields = ('id', 'lastname', 'firstname', 'gender', 'promotion', 'email_junior', 'mobile', 'address', 'postcode', 'town', 'country', 'nationality', 'birth_date', 'birth_place', 'email', 'user')

