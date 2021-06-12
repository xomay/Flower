from django.db import models
from datetime import date
from rest_framework import serializers

from .Etude import Etude
from .People.Membre import Membre
from .People.Employe import Employe
from .GroupePhase import GroupesSet, GroupesSetSerializer

def createNewGS():
    return GroupesSet.objects.create().id

def getNewNumber(project):
    return project.avenant_set.count() + 1

class Avenant(models.Model):
    # Étude concernée
    project = models.ForeignKey(Etude, on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField(null=True, blank=True, default=0) # numéro dans l'étude. Remplie par le serializer. Si == 0 c'est vide
    comment = models.TextField(null=True,blank=True) # un commentaire optionnel pouvant être laissé par le chargé
    # Signataires
    signataire_junior = models.ForeignKey(Membre, on_delete=models.CASCADE)
    signataire_prospect = models.ForeignKey(Employe, on_delete=models.CASCADE)
    # Un avenant peut cumuler plusieurs types.
    is_delais = models.BooleanField(default=False)      # Si cet avenant modifie les délais de l'étude
    is_methodo = models.BooleanField(default=False)     # Si cet avenant modifie les phases de l'étude
    is_cdc = models.BooleanField(default=False)         # Si cet avenant modifie le cahier des charges
    is_budget = models.BooleanField(default=False)      # Si cet avenant modifie le budget des phases
    # Date de la signature
    signature_date = models.DateField()
    # Modifications
    groupes = models.ForeignKey(GroupesSet, default=createNewGS, on_delete=models.RESTRICT)
    new_dates = models.DateField(null=True, blank=True) # si délais

    @property
    def hasGroupes(self):
        return self.groupes != None

    @property
    def reference(self):
        modes = str(
            (('', 'D,')[self.is_delais]) + 
            (('', 'M,')[self.is_methodo]) +
            (('', 'C,')[self.is_cdc]) +
            (('', 'B,')[self.is_budget])
        )[:-1]
        return 'AV' + str(self.number) + '-' + modes + '_' + str(self.project.number)

    def __str__(self):
        return "Avenant["+self.project.name+"]:"+self.reference
    
class AvenantSerializer(serializers.ModelSerializer):
    reference = serializers.ReadOnlyField()
    hasGroupes = serializers.ReadOnlyField()
    groupes = GroupesSetSerializer(read_only=True)
    class Meta:
        model = Avenant
        fields = '__all__'

class ShortAvenantSerializer(serializers.ModelSerializer):
    reference = serializers.ReadOnlyField()
    hasGroupes = serializers.ReadOnlyField()
    class Meta:
        model = Avenant
        fields = '__all__'