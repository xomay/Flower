from django.db import models
from rest_framework import serializers

from .CC import CC
from .People.Employe import Employe, EmployeSerializer
from .People.Membre import Membre, MembreSerializer

# Create your models here.
class DocEtude(models.Model):
    signer1 = models.ForeignKey(Membre, on_delete=models.RESTRICT, blank=True, null=True)
    signer2 = models.ForeignKey(Employe, on_delete=models.RESTRICT, blank=True, null=True)
    signDate = models.DateTimeField(blank=True, null=True)
    deposit = models.BooleanField(default=True)
    depositAmount = models.DecimalField(default=30, max_digits=10, decimal_places=2)
    consultantNumber = models.IntegerField(default=1)
    description = models.TextField(default='')
    # spec = cdc
    spec = models.TextField(default='')
    controls = models.JSONField(default=list, blank=True)
    deliverable = models.TextField(default='')
    real_desc = models.TextField(default='')
    hasMaterialFees = models.BooleanField(default=False)
    materialFees = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    materialDesc = models.TextField(default='')

    def __str__(self):
        return 'CE'

class CESerializer(serializers.ModelSerializer):
    class Meta:
        model = DocEtude
        fields = '__all__'

class CEDetailSerializer(serializers.ModelSerializer):
    signer1 = MembreSerializer(read_only=True)
    signer2 = EmployeSerializer(read_only=True)
    class Meta:
        model = DocEtude
        fields = '__all__'