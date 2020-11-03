from django.db import models

from rest_framework import serializers

from flower_app.models.People.Prospect import Prospect
from flower_app.models.People.Personne import Personne

# An employee is a Personne from a Prospect
class Employe(Personne):
    prospect = models.ForeignKey(Prospect, on_delete=models.RESTRICT)
    lastname = models.CharField(max_length=60)
    firstname = models.CharField(max_length=60)
    position = models.CharField(max_length=200)

    def __str__(self):
        return self.firstname + ' ' + self.lastname

class EmployeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employe
        fields = '__all__'
