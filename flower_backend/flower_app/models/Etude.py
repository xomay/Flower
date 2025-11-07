from django.db import models
from rest_framework import serializers

from .CC import CC
from .People.Employe import Employe, EmployeSerializer
from .People.Membre import Membre, MembreSerializer
from .People.Prospect import Prospect, ProspectSerializer
from .DocEtude import DocEtude, CEDetailSerializer
from .UploadedFile import UploadedFile, UploadedFileSerializer

from decimal import Decimal

def create_doc():
    return DocEtude.objects.create().id

# Create your models here.
class Etude(models.Model):
    mandat = models.IntegerField()
    number = models.IntegerField()
    name = models.CharField(max_length=60)
    description = models.TextField(blank=True,default='')
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    # State < 0 : étude avortée
    # State dans [0,9] : en cours
    # State == 10 : étude terminée
    state = models.IntegerField(default=0)
    qualiValidatePeda = models.BooleanField(default=False)
    confidential = models.BooleanField()
    audit_date = models.DateField(blank=True, null=True)

    prospect = models.ForeignKey(Prospect, on_delete=models.RESTRICT)
    qualityManager = models.ForeignKey(Membre, on_delete=models.RESTRICT, related_name="qualityManager", blank=True, null=True)
    projectManager = models.ForeignKey(Membre, on_delete=models.RESTRICT, related_name="projectManager", blank=True, null=True)
    clientContact = models.ForeignKey(Employe, on_delete=models.RESTRICT, blank=True, null=True)
    
    docEtude = models.OneToOneField(DocEtude, on_delete=models.CASCADE, blank=True, null=True, default=create_doc)
    cc = models.ForeignKey(CC, on_delete=models.RESTRICT, blank=True, null=True)

    
    linkedFiles = models.ManyToManyField(UploadedFile, blank=True)

    def __str__(self):
        if(self.isAborted):
            state = "[avortée]"
        elif(self.isFinished):
            state = "[finie]"
        else:
            state = ""
        return "Étude '"+self.name + "' " + state

    @property
    def phases(self):
        #return self.phasesEtude.all()
        return self.phaseEtude.filter(state='ACTIVE')

    @property
    def isAborted(self):
        return self.state < 0
    @property
    def isFinished(self):
        return self.state >= 10
    
    # Indique si l'on peut modifier les phases, les RDM, les factures, ... liés à cette étude. Les fields, eux, peuvent être modifiés.
    # Pour l'instant, une étude reste modifiable même après qu'elle soit terminée.
    # Ainsi, on interdit seulement les modifs une fois l'étude avortée. À voir si on change ça après ou pas.
    @property
    def canBeEdited(self):
        return not self.isAborted

    @property
    def ceReference(self):
        return 'CE_' + str(self.number)

    @property
    def nbJEH(self):
        total = 0
        for phase in self.phases.all():
            total += phase.nbJEH
        return total
        
    @property
    def nbPhases(self):
        total = 0
        return len(self.phases.all())

    @property
    def totalPrice(self):
        total = 0
        for phase in self.phases.all():
            total += phase.totalPrice
        return total

    @property
    def totalTaxes(self):
        return round(self.totalPrice * Decimal('0.2'), 2)

    @property
    def totalPriceTaxes(self):
        return round(self.totalPrice * Decimal('1.2'), 2)

class SimuEtude(Etude):
    class Meta:
        verbose_name = "SimuÉtude"
        verbose_name_plural = "SimuÉtudes"

class EtudeSerializer(serializers.ModelSerializer):
    isAborted = serializers.SerializerMethodField()
    isFinished = serializers.SerializerMethodField()
    def get_avenantsAmount(self, instance):
        return instance.avenant_set.count()
    def get_isAborted(self, instance):
        return instance.isAborted
    def get_isFinished(self, instance):
        return instance.isFinished
    class Meta:
        model = Etude
        fields = '__all__'

class EtudeDetailSerializer(serializers.ModelSerializer):
    projectManager = MembreSerializer(read_only=True)
    qualityManager = MembreSerializer(read_only=True)
    prospect = ProspectSerializer(read_only=True)
    clientContact = EmployeSerializer(read_only=True)
    linkedFiles = UploadedFileSerializer(many=True, read_only=True)
    bvData = serializers.SerializerMethodField()
    isAborted = serializers.SerializerMethodField()
    isFinished = serializers.SerializerMethodField()
    docEtude = CEDetailSerializer(read_only=True)
    missions = serializers.SerializerMethodField()
    invoices = serializers.SerializerMethodField()
    pvr = serializers.SerializerMethodField()
    phases = serializers.SerializerMethodField()
    avenants = serializers.SerializerMethodField()
    requirements = serializers.SerializerMethodField()

    def get_isAborted(self, instance):
        return instance.isAborted

    def get_isFinished(self, instance):
        return instance.isFinished

    def get_bvData(self, instance):
        data = {}
        full = True
        for rdm in instance.mission_set.all():
            if len(rdm.bv_set.all()) > 0:
                data[str(rdm.id)] = rdm.bv_set.first().id
            else:
                data[str(rdm.id)] = -1
                full = False
        data['full'] = full
        return data

    def get_missions(self, instance):
        from .Mission import MissionDetailSerializer
        return MissionDetailSerializer(instance.mission_set.all(), many=True).data

    def get_invoices(self, instance):
        from .Facture import FactureSerializer
        return FactureSerializer(instance.facture_set.all(), many=True).data

    def get_pvr(self, instance):
        from .PVR import PVRSerializer
        return PVRSerializer(instance.pvr_set.all(), many=True).data

    def get_phases(self, instance):
        from .GroupePhase import PhaseEtudeSerializer
        return PhaseEtudeSerializer(instance.phaseEtude.filter(state='ACTIVE'), many=True).data

    def get_avenants(self, instance):
        from .Avenant import AvenantEtudeDetailSerializer
        return AvenantEtudeDetailSerializer(instance.avenantsEtude.all(), many=True).data

    def get_requirements(self, instance):
        from .Requirement import RequirementSerializer
        return RequirementSerializer(instance.requirements.all(), many=True).data

    class Meta:
        model = Etude
        fields = '__all__'
