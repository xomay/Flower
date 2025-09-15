from django.db import models
from rest_framework import serializers

from .DocEtude import DocMission, DocMissionSerializer
from .Etude import Etude
from .People.Realisateur import Realisateur, RealisateurSerializer
from ..serializers import CustomListSerializer
from .BaseUrsaff import getLastBase

def emptyList():
    return []

#def generateNumberYear():
#    Mission = apps.get_model(app_label='flower_app', model_name='Mission')
#    year = datetime.datetime.now().year
#    number = 1
#    for rdm in Mission.objects.all():
#        if(rdm.project.mandat == year):
#            number = number + 1
#    return number

def create_doc():
    return DocMission.objects.create().id

class Mission(models.Model):
    consultant = models.ForeignKey(Realisateur, on_delete=models.RESTRICT, blank=True, null=True)
    missionBegin = models.DateField(blank=True, null=True)
    missionEnd = models.DateField(blank=True, null=True)
    percentageJunior = models.FloatField(default=0.51)
    JEH_price = models.IntegerField(default=220)
    project = models.ForeignKey(Etude, on_delete=models.RESTRICT)
    doc_mission = models.OneToOneField(DocMission, on_delete=models.CASCADE, blank=True, null=True)
#    number_this_year = models.IntegerField(default=generateNumberYear)

    def __str__(self):
        prefix = ""
        return prefix + "[RDM]" + str(self.project) + ", réa=" + str(self.consultant) + ", (" + str(self.JEHNumber) + "JEH,  " + str(self.remunerationRaw) + "€)"

    @property
    def phases(self):
        return self.phasesMission.all()

    @property
    def JEHNumber(self):
        amount = 0
        for phase in self.phases.all():
            amount += phase.nbJEH
        return amount
    
    @property
    def totalPrice(self):
        amount = 0
        for phase in self.phases.all():
            amount += phase.totalPrice
        return amount

    @property
    def remunerationRaw(self):
        #return round((1 - float(self.percentageJunior)) * float(self.totalPrice), 2)
        return self.totalPrice

    def save(self, *args, **kwargs):
        if not self.doc_mission:
            self.doc_mission = DocMission.objects.create().id
        super().save(*args, **kwargs)


#    @property
#    def reference(self):
#        n_prefix = ""
#        if self.number_this_year < 10:
#            n_prefix = "00"
#        elif self.number_this_year < 100:
#            n_prefix = "0"
#        return "RDM_" + str(self.project.mandat)[-2:] + n_prefix + str(self.number_this_year)

class MissionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, write_only=False)
    isCurrent = serializers.ReadOnlyField()
    remunerationRaw = serializers.ReadOnlyField()
    JEHNumber = serializers.ReadOnlyField()
    class Meta:
        model = Mission
        fields = '__all__'
        list_serializer_class = CustomListSerializer


class MissionDetailSerializer(serializers.ModelSerializer):
    consultant = RealisateurSerializer(read_only=True)
    remunerationRaw = serializers.ReadOnlyField()
    JEHNumber = serializers.ReadOnlyField()
    assietteCotisation = serializers.SerializerMethodField()
    bv_id = serializers.SerializerMethodField()
    isCurrent = serializers.ReadOnlyField()
    phasesMission = serializers.SerializerMethodField()
    doc_mission = DocMissionSerializer(read_only=True)
    avenants = serializers.SerializerMethodField()

    class Meta:
        model = Mission
        fields = '__all__'

    def get_assietteCotisation(self, obj):
        return getLastBase().baseValue * obj.JEHNumber

    def get_bv_id(self, obj):
        if(obj.bv_set.count() == 0):
            return -1
        return obj.bv_set.first().id

    def get_avenants(self, instance):
        from .Avenant import AvenantMissionDetailSerializer
        return AvenantMissionDetailSerializer(instance.avenantsMission.all(), many=True).data

    def get_phasesMission(self, instance):
        from .GroupePhase import PhaseMissionSerializer
        return PhaseMissionSerializer(instance.phasesMission.filter(state='ACTIVE'), many=True).data