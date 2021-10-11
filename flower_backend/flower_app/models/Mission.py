from django.db import models
from rest_framework import serializers

from .People.Realisateur import Realisateur, RealisateurSerializer
from .Etude import Etude
from .GroupePhase import GroupesSetSerializer, Phase
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

class Mission(models.Model):
    project = models.ForeignKey(Etude, on_delete=models.RESTRICT)
    consultant = models.ForeignKey(Realisateur, on_delete=models.RESTRICT, blank=True, null=True)
    missionBegin = models.DateField(blank=True, null=True)
    missionEnd = models.DateField(blank=True, null=True)
    percentageJunior = models.FloatField(default=0.55)
    JEHNumber = models.IntegerField(default=1)
    phases = models.ManyToManyField(Phase, default=emptyList, blank=True)
#    number_this_year = models.IntegerField(default=generateNumberYear)

    @property
    def groupeSet(self):
        return self.phases.first().groupe.owner

    def __str__(self):
        return 'Mission - Etude = ' + str(self.project) + ' - Consultant = ' + str(self.consultant) + ' (' + str(self.JEHNumber) + 'JEH,  ' + str(self.remunerationRaw) + '€)'
    
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
        return (1 - float(self.percentageJunior)) * float(self.totalPrice)
    
    @property
    def isCurrent(self):
        return self.groupeSet.id == self.project.currentGroupes.id

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
    groupeSetId = serializers.SerializerMethodField()
    isCurrent = serializers.ReadOnlyField()
    remunerationRaw = serializers.ReadOnlyField()
    JEHNumber = serializers.ReadOnlyField()
    def get_groupeSetId(self, obj):
        return obj.groupeSet.id
    class Meta:
        model = Mission
        fields = '__all__'
        list_serializer_class = CustomListSerializer

class MissionDetailSerializer(serializers.ModelSerializer):
    consultant = RealisateurSerializer(read_only=True)
    remunerationRaw = serializers.ReadOnlyField()
    JEHNumber = serializers.ReadOnlyField()
    assietteCotisation = serializers.SerializerMethodField()
    groupeSet = GroupesSetSerializer(read_only=True)
    bv_id = serializers.SerializerMethodField()
    isCurrent = serializers.ReadOnlyField()
    class Meta:
        model = Mission
        fields = '__all__'
    def get_assietteCotisation(self, obj):
        return getLastBase().baseValue * obj.JEHNumber
    def get_bv_id(self, obj):
        if(obj.bv_set.count() == 0):
            return -1
        return obj.bv_set.first().id