from django.db import models
from rest_framework import serializers
import datetime
from django.apps import apps

from flower_app.models.People.Realisateur import Realisateur, RealisateurSerializer
from flower_app.models.Etude import Etude
from flower_app.models.GroupePhase import Phase
from flower_app.serializers import CustomListSerializer
from flower_app.models.BaseUrsaff import getLastBase

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
    JEHPrice = models.DecimalField(default=400, max_digits=10, decimal_places=2)
    phases = models.ManyToManyField(Phase, default=emptyList, blank=True)
#    number_this_year = models.IntegerField(default=generateNumberYear)

    def __str__(self):
        return 'Mission - Etude = ' + str(self.project) + ' - Consultant = ' + str(self.consultant) + ' (' + str(self.JEHNumber) + ' * ' + str(self.JEHPrice) + '€)'
    
    @property
    def remunerationRaw(self):
        return self.JEHNumber * self.JEHPrice

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
    class Meta:
        model = Mission
        fields = '__all__'
        list_serializer_class = CustomListSerializer

class MissionDetailSerializer(serializers.ModelSerializer):
    consultant = RealisateurSerializer(read_only=True)
    remunerationRaw = serializers.SerializerMethodField()
    assietteCotisation = serializers.SerializerMethodField()
    bv_id = serializers.SerializerMethodField()
    class Meta:
        model = Mission
        fields = '__all__'
    def get_remunerationRaw(self, obj):
        return obj.remunerationRaw
    def get_assietteCotisation(self, obj):
        return getLastBase().baseValue * obj.JEHNumber
    def get_bv_id(self, obj):
        if(obj.bv_set.count() == 0):
            return -1
        return obj.bv_set.first().id