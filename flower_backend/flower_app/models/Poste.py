from django.db import models
from rest_framework import serializers
from django.contrib.auth.models import Permission, Group

class Poste(models.Model):
    name = models.CharField(max_length=60)
    name_feminine = models.CharField(max_length=60, blank=True)
    subordinates = models.ManyToManyField("Poste", blank=True)
    role = models.ManyToManyField(Group, blank = True)

    def __str__(self):
        return self.name + "( -> " + str(len(self.subordinates.all())) + " )"
    
    def get_permissions(self):
        return []


class PosteSerializer(serializers.ModelSerializer):
    role = serializers.SlugRelatedField(
        many=True, 
        queryset=Group.objects.all(), 
        slug_field="name"
    )

    class Meta:
        model = Poste
        fields = '__all__'

