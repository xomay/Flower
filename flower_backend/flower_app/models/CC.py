from django.db import models
from rest_framework import serializers

from .People.Employe import Employe, EmployeSerializer
from .People.Membre import Membre, MembreSerializer

# Create your models here.
class CC(models.Model):
    signer1 = models.ForeignKey(Membre, on_delete=models.RESTRICT, blank=True, null=True)
    signer2 = models.ForeignKey(Employe, on_delete=models.RESTRICT, blank=True, null=True)
    signDate = models.DateTimeField(blank=True, null=True)
    period = models.IntegerField(default=2)
    name = models.CharField(max_length=60)
    description = models.TextField(blank=True,default='')
    confidential = models.BooleanField()

    def __str__(self):
        return 'CC'

class CCSerializer(serializers.ModelSerializer):
    class Meta:
        model = CC
        fields = '__all__'

class CCDetailSerializer(serializers.ModelSerializer):
    signer1 = MembreSerializer(read_only=True)
    signer2 = EmployeSerializer(read_only=True)
    class Meta:
        model = CC
        fields = '__all__'