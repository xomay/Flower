from django.db import models
from rest_framework import serializers

from .CC import CC
from .People.Employe import Employe, EmployeSerializer
from .People.Membre import Membre, MembreSerializer

class Doc(models.Model):
    signDate = models.DateTimeField(blank=True, null=True)
    description = models.TextField(default='')
    controls = models.JSONField(default=list, blank=True)
    deliverable = models.TextField(default='')
    materialDesc = models.TextField(default='', blank=True)

    def __str__(self):
        return 'CE'

    class Meta:
        abstract = True

class DocEtude(Doc):
    signer1 = models.ForeignKey(Membre, on_delete=models.RESTRICT, blank=True, null=True)
    signer2 = models.ForeignKey(Employe, on_delete=models.RESTRICT, blank=True, null=True)
    deposit = models.BooleanField(default=True)
    depositAmount = models.DecimalField(default=30, max_digits=10, decimal_places=2)
    consultantNumber = models.IntegerField(default=1)
    real_desc = models.TextField(default='')
    hasMaterialFees = models.BooleanField(default=False)
    materialFees = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    application_fees = models.DecimalField(default=0, max_digits=10, decimal_places=2)

    def __str__(self):
        return 'CE'

class CESerializer(serializers.ModelSerializer):
    class Meta:
        model = DocEtude
        fields = '__all__'

    def update(self, instance, validated_data):
        from .GroupePhase import PhaseEtude
        from .Avenant import AvenantEtude

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        avenant = AvenantEtude.objects.get(doc_etude=instance)

        if avenant and instance.signDate is not None:
            print("Avenant signé")
            PhaseEtude.objects.filter(avenant_edit=avenant, state='ACTIVE').update(state='CANCELED')
            PhaseEtude.objects.filter(avenant_creer=avenant, state='PENDING').update(state='ACTIVE')
        elif avenant:
            print("Avenant en cours d'édition")
            PhaseEtude.objects.filter(avenant_edit=avenant).update(state='ACTIVE')
            PhaseEtude.objects.filter(avenant_creer=avenant, state='ACTIVE').update(state='PENDING')

        return instance

class CEDetailSerializer(serializers.ModelSerializer):
    signer1 = MembreSerializer(read_only=True)
    signer2 = EmployeSerializer(read_only=True)
    class Meta:
        model = DocEtude
        fields = '__all__'

class DocMission(Doc):

    def __str__(self):
        return 'Doc Mission'

class DocMissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocMission
        fields = '__all__'

    def update(self, instance, validated_data):
        from .GroupePhase import PhaseMission
        from .Avenant import AvenantMission

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        avenant = AvenantMission.objects.get(doc_mission=instance)

        if avenant and instance.signDate is not None:
            print("Avenant signé")
            PhaseMission.objects.filter(avenant_edit=avenant, state='ACTIVE').update(state='CANCELED')
            PhaseMission.objects.filter(avenant_creer=avenant, state='PENDING').update(state='ACTIVE')
        elif avenant:
            print("Avenant en cours d'édition")
            PhaseMission.objects.filter(avenant_edit=avenant).update(state='ACTIVE')
            PhaseMission.objects.filter(avenant_creer=avenant, state='ACTIVE').update(state='PENDING')

        return instance