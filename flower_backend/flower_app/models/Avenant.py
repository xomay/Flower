from django.db import models
from datetime import date
from rest_framework import serializers

from .Etude import Etude
from .People.Membre import Membre
from .People.Employe import Employe
from .GroupePhase import Groupe, GroupesSet, GroupesSetSerializer, Phase, US

def createNewGS():
    return GroupesSet.objects.create().id

def getNewNumber(project):
    return project.avenant_set.count() + 1

class Avenant(models.Model):
    # Étude concernée
    project = models.ForeignKey(Etude, on_delete=models.CASCADE)
    author = models.ForeignKey(Membre, on_delete=models.SET_NULL, null=True, related_name="avenants_made")
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
        return (self.groupes != None) and (self.groupes.groupe_set.count() > 0)

    # Mirror the owner's #canBeEdited property. Used by GroupeSet.
    @property
    def canBeEdited(self):
        return self.project.canBeEdited

    @property
    def reference(self):
        modes = str(
            (('', 'D,')[self.is_delais]) + 
            (('', 'M,')[self.is_methodo]) +
            (('', 'C,')[self.is_cdc]) +
            (('', 'B,')[self.is_budget])
        )[:-1] # le [:-1] sert, bien évidemment, à retirer la virgule en rab'
        return 'AV' + str(self.number) + '-' + modes + '_' + str(self.project.number)

    def __str__(self):
        return "Avenant["+self.project.name+"]:"+self.reference
    
    def delete(self):
        #Delete also US, Phases and Groupes
        groupeset_id = self.groupes.id
        for us in US.objects.all():
            if us.phase.groupe.owner.id == groupeset_id:
                us.delete()
        for phase in Phase.objects.all():
            if phase.groupe.owner.id == groupeset_id:
                phase.delete()
        for groupe in Groupe.objects.all():
            if groupe.owner.id == groupeset_id:
                groupe.delete()
        # Delete avevant
        super(Avenant, self).delete()
        # Delete GS
        GroupesSet.objects.get(pk=groupeset_id).delete()
    
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