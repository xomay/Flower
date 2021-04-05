from django.db import models
from rest_framework import serializers

from flower_app.models.People.Realisateur import Realisateur, RealisateurSerializer
from flower_app.models.Etude import Etude
from flower_app.models.GroupePhase import Phase
from flower_app.serializers import CustomListSerializer
from flower_app.models.BaseUrsaff import getLastBase

def emptyList():
    return []

class Mission(models.Model):
    project = models.ForeignKey(Etude, on_delete=models.RESTRICT)
    consultant = models.ForeignKey(Realisateur, on_delete=models.RESTRICT, blank=True, null=True)
    missionBegin = models.DateField(blank=True, null=True)
    missionEnd = models.DateField(blank=True, null=True)
    percentageJunior = models.FloatField(default=0.55)
    JEHNumber = models.IntegerField(default=1)
    JEHPrice = models.DecimalField(default=400, max_digits=10, decimal_places=2)
    phases = models.ManyToManyField(Phase, default=emptyList, blank=True)

    def __str__(self):
        return 'Mission - Etude = ' + str(self.project) + ' - Consultant = ' + str(self.consultant) + ' (' + str(self.JEHNumber) + ' * ' + str(self.JEHPrice) + '€)'
    
    @property
    def remunerationRaw(self):
        return self.JEHNumber * self.JEHPrice

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
    class Meta:
        model = Mission
        fields = '__all__'
    def get_remunerationRaw(self, obj):
        return obj.remunerationRaw
    def get_assietteCotisation(self, obj):
        return getLastBase().baseValue * obj.JEHNumber