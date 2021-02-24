from django.db import models
from rest_framework import serializers
from flower_app.models.People.Membre import Membre, MembreSerializer
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal

class NdF(models.Model):
    demandeur = models.ForeignKey(Membre, on_delete=models.RESTRICT)
    mandat = models.IntegerField(default=2021, validators=[MinValueValidator(2020), MaxValueValidator(2100)])
    date = models.DateField()
    objet = models.TextField()
    numberThisYear = models.IntegerField(default=1, validators=[MinValueValidator(0), MaxValueValidator(999)])

    @property
    def montantHT(self):
        total = Decimal(0)
        for detail in getattr(self, 'ndfdetail_set').all():
            if(detail.isKilometrique):
                total += Decimal(detail.montantTTC)
            else:
                total += Decimal(detail.prixHT)
        return total

    @property
    def montantTVA(self):
        total = Decimal(0)
        for detail in getattr(self, 'ndfdetail_set').all():
            total += Decimal(detail.montantTVA)
        return total

    @property
    def montantTTC(self):
        total = Decimal(0)
        for detail in getattr(self, 'ndfdetail_set').all():
            total += Decimal(detail.montantTTC)
        return total

    @property
    def isKilometrique(self):
        for detail in getattr(self, 'ndfdetail_set').all():
            if(detail.isKilometrique):
                return True
        return False

    def niceMembre(self):
        return self.demandeur.firstname.capitalize()[0] + self.demandeur.lastname.capitalize()[0] # + le numéro

    def niceNumberInYear(self):
        number = self.numberThisYear
        if(number < 10):
            return '00'+str(number)
        elif(number < 100):
            return '0'+str(number)
        return str(number) 

    @property
    def reference(self):
        return str(self.mandat)[-2:] + '-NF' + self.niceNumberInYear() + "-" + self.niceMembre()
        
    def __str__(self):
        return self.reference
    
    class Meta:
       verbose_name = 'Note de Frais'
       verbose_name_plural = 'Notes de Frais'

from flower_app.models.NdFDetail import NdFDetailSerializer

class NdFSerializer(serializers.ModelSerializer):
    # Ajout des propeties
    reference = serializers.SerializerMethodField()
    isKilometrique = serializers.SerializerMethodField()
    montantHT = serializers.SerializerMethodField()
    montantTVA = serializers.SerializerMethodField()
    montantTTC = serializers.SerializerMethodField()
    # Re-sérialisation
    demandeur = MembreSerializer(read_only=True)
    details = NdFDetailSerializer(source='ndfdetail_set', many=True, read_only=True)
    class Meta:
        model = NdF
        fields = '__all__'
    def get_reference(self, obj):
        return obj.reference
    def get_isKilometrique(self, obj):
        return obj.isKilometrique
    def get_montantHT(self, obj):
        return obj.montantHT
    def get_montantTVA(self, obj):
        return obj.montantTVA
    def get_montantTTC(self, obj):
        return obj.montantTTC
