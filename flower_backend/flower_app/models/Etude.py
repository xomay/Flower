from django.db import models
from rest_framework import serializers

from .People.Employe import Employe, EmployeSerializer
from .People.Membre import Membre, MembreSerializer
from .People.Prospect import Prospect, ProspectSerializer
from .CE import CE
from .UploadedFile import UploadedFile, UploadedFileSerializer
from .GroupePhase import GroupesSet

from decimal import Decimal

def create_ce():
    return CE.objects.create().id
def create_groupesset():
    return GroupesSet.objects.create().id

# Create your models here.
class Etude(models.Model):
    mandat = models.IntegerField()
    number = models.IntegerField()
    name = models.CharField(max_length=60)
    description = models.TextField(blank=True,default='')

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    state = models.IntegerField(default=0)
    qualiValidatePeda = models.BooleanField(default=False)
    confidential = models.BooleanField()
    audit_date = models.DateField(blank=True, null=True)

    prospect = models.ForeignKey(Prospect, on_delete=models.RESTRICT)
    qualityManager = models.ForeignKey(Membre, on_delete=models.RESTRICT, related_name="qualityManager", blank=True, null=True)
    projectManager = models.ForeignKey(Membre, on_delete=models.RESTRICT, related_name="projectManager", blank=True, null=True)
    clientContact = models.ForeignKey(Employe, on_delete=models.RESTRICT, blank=True, null=True)
    
    ce = models.OneToOneField(CE, default=create_ce, on_delete=models.CASCADE)

    # Set de groupes de phases par défaut (structure originale)
    originalGroupes = models.ForeignKey(GroupesSet, default=create_groupesset, on_delete=models.RESTRICT)
    # Avenants :
    # dans 'avenant_set'

    deposit_percentage = models.DecimalField(default=30, max_digits=10, decimal_places=2)
    deposit_sum = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    application_fees = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    
    linkedFiles = models.ManyToManyField(UploadedFile, blank=True)

    def __str__(self):
        return "Étude : "+self.name

    @property
    def ceReference(self):
        return 'CE_' + self.number

    @property
    def nbJEH(self):
        total = 0
        for groupe in self.groupes.groupe_set.iterator():
            total += groupe.nbJEH
        return total

    @property
    def totalPrice(self):
        total = 0
        for groupe in self.groupes.groupe_set.iterator():
            total += groupe.totalPrice
        return total

    @property
    def totalTaxes(self):
        return round(self.totalPrice * Decimal('0.2'), 2)

    @property
    def totalPriceTaxes(self):
        return round(self.totalPrice * Decimal('1.2'), 2)

    @property
    def currentGroupes(self):
        if hasattr(self, 'avenant_set'):
            if self.avenant_set.count() > 0:
                # on renvoie le 1er avenant parmi les derniers qui possède une structure de groupes
                for avenant in self.avenant_set.order_by('-id').all():
                    if avenant.hasGroupes:
                        return avenant.groupes
        return self.originalGroupes

class EtudeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etude
        fields = '__all__'


# Can only be imported once the Etude model is completely defined ! 
from .Mission import MissionDetailSerializer
from .Avenant import ShortAvenantSerializer
from .GroupePhase import GroupesSet, GroupesSetSerializer
from .Facture import FactureSerializer
from .PVR import PVRSerializer

class EtudeDetailSerializer(serializers.ModelSerializer):
    projectManager = MembreSerializer(read_only=True)
    qualityManager = MembreSerializer(read_only=True)
    prospect = ProspectSerializer(read_only=True)
    clientContact = EmployeSerializer(read_only=True)
    missions = MissionDetailSerializer(source='mission_set', many=True, read_only=True)
    invoices = FactureSerializer(source='facture_set', many=True, read_only=True)
    avenants = ShortAvenantSerializer(source='avenant_set', many=True, read_only=True)
    pvr = PVRSerializer(source='pvr_set', many=True, read_only=True)
    linkedFiles = UploadedFileSerializer(many=True, read_only=True)
    bvData = serializers.SerializerMethodField()
    currentGroupes = serializers.SerializerMethodField()
    isOriginalGroupes = serializers.SerializerMethodField()
    def get_isOriginalGroupes(self, instance):
        return instance.currentGroupes.id == instance.originalGroupes.id
    def get_currentGroupes(self, instance):
        return GroupesSetSerializer(instance.currentGroupes, read_only=True).data
    def get_bvData(self, instance):
        data = {}
        full = True
        for rdm in instance.mission_set.all():
            if len(rdm.bv_set.all()) > 0:
                data[str(rdm.id)] = rdm.bv_set.first().id # il n'y a que un BV par RdM
            else:
                data[str(rdm.id)] = -1
                full = False
        data['full'] = full
        return data
    class Meta:
        model = Etude
        exclude = ('originalGroupes',) # on ne veut juste pas sérializer le groupe original : le vrai groupe est le currentGroup ! :o
