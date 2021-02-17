from django.db import models
from rest_framework import serializers

from flower_app.models.CE import CE
from flower_app.models.People.Employe import Employe
from flower_app.models.People.Membre import Membre, MembreSerializer
from flower_app.models.People.Prospect import Prospect, ProspectSerializer

from decimal import Decimal

def create_ce():
    return CE.objects.create().id

# Create your models here.
class Etude(models.Model):
    mandat = models.IntegerField()
    number = models.IntegerField()
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=300)

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    state = models.IntegerField(default=0)
    confidential = models.BooleanField()
    audit_date = models.DateField(blank=True, null=True)

    prospect = models.ForeignKey(Prospect, on_delete=models.RESTRICT)
    qualityManager = models.ForeignKey(Membre, on_delete=models.RESTRICT, related_name="qualityManager", blank=True, null=True)
    projectManager = models.ForeignKey(Membre, on_delete=models.RESTRICT, related_name="projectManager", blank=True, null=True)
    clientContact = models.ForeignKey(Employe, on_delete=models.RESTRICT, blank=True, null=True)
    
    ce = models.OneToOneField(CE, default=create_ce, on_delete=models.CASCADE)
    # ce
    # facture
    # avenants
    # phases
    # RDM

    deposit_percentage = models.DecimalField(default=30, max_digits=10, decimal_places=2)
    deposit_sum = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    application_fees = models.DecimalField(default=0, max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    @property
    def ceReference(self):
        return 'CE_' + self.number

    @property
    def nbJEH(self):
        total = 0
        for groupe in self.groupe_set.iterator():
            total += groupe.nbJEH
        return total

    @property
    def totalPrice(self):
        total = 0
        for groupe in self.groupe_set.iterator():
            total += groupe.totalPrice
        return total

    @property
    def totalTaxes(self):
        return round(self.totalPrice * Decimal('0.2'), 2)

    @property
    def totalPriceTaxes(self):
        return round(self.totalPrice * Decimal('1.2'), 2)

class EtudeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etude
        fields = '__all__'


# Can only be imported once the Etude model is completely defined ! 
from flower_app.models.Mission import Mission, MissionSerializer, MissionDetailSerializer

from flower_app.models.GroupePhase import Groupe, GroupeDetailSerializer
from flower_app.models.Facture import FactureSerializer
from flower_app.models.PVR import PVRSerializer

class EtudeDetailSerializer(serializers.ModelSerializer):
    projectManager = MembreSerializer(read_only=True)
    qualityManager = MembreSerializer(read_only=True)
    prospect = ProspectSerializer(read_only=True)
    missions = MissionDetailSerializer(source='mission_set', many=True, read_only=True)
    groupes = GroupeDetailSerializer(source='groupe_set', many=True, read_only=True)
    invoices = FactureSerializer(source='facture_set', many=True, read_only=True)
    pvr = PVRSerializer(source='pvr_set', many=True, read_only=True)
    class Meta:
        model = Etude
        fields = '__all__'

