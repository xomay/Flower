from django.db import models
from django.db.models.deletion import RESTRICT
from rest_framework import serializers

from .Avenant import Avenant
from ..serializers import CustomListSerializer
from datetime import date, timedelta

class Phase(models.Model):
    title = models.CharField(max_length=200, default='Titre')
    index = models.IntegerField()
    description = models.TextField(default='')
    methodologie = models.TextField(blank=True, default='')

    period = models.IntegerField(default=14)
    
    nbJEH = models.IntegerField(default=1)
    priceJEH = models.DecimalField(default=450, max_digits=10, decimal_places=2)

    # spec = cdc
    spec = models.TextField(default='', blank=True)

    avenant_creer = models.ForeignKey(Avenant, on_delete=models.CASCADE, blank=True, null=True, related_name='avenantCreator')
    avenant_edit = models.ForeignKey(Avenant, on_delete=models.SET_NULL, blank=True, null=True, related_name='avenantEdit')

    CHOICES_STATES = [
        ('CANCELED', 'CANCELED'),
        ('PENDING', 'PENDING'),
        ('ACTIVE', 'ACTIVE')
    ]
    state = models.CharField(max_length=10, choices=CHOICES_STATES, default='ACTIVE')


    def __str__(self):
        return self.title

    @property
    def totalPrice(self):
        return self.nbJEH * self.priceJEH

class PhaseEtude(Phase):
    from .Etude import Etude
    etude = models.ForeignKey(Etude, on_delete=models.RESTRICT, related_name='phaseEtude')

class PhaseMission(Phase):
    from .Mission import Mission
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name='phasesMission')
    phaseEtude = models.ForeignKey(PhaseEtude, on_delete=models.CASCADE, related_name='phasesEtudeAssociate', null=True)

class US(models.Model):
    name = models.CharField(max_length=200, null=False)
    index = models.IntegerField()
    US_STATES = [
        ('DEFIN', 'En cours de définition'),
        ('TODO', 'À faire'),
        ('DOING', 'En train d\'être fait'),
        ('DONE', 'Fait'),
        ('REDO', 'À modifier'),
        ('OVER', 'Validé')
    ]
    state = models.CharField(max_length=5, choices=US_STATES, default='DEFIN')
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE)
    def __str__(self):
        return "US(" + str(self.phase.__str__()) + ")["+self.name+"]"
    class Meta:
       verbose_name = 'US'
       verbose_name_plural = 'US'

class USSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, write_only=False)
    class Meta:
        model = US
        fields = '__all__'
        list_serializer_class = CustomListSerializer

class PhaseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, write_only=False)
    uss = USSerializer(source='us_set' ,many=True)
    totalPrice = serializers.SerializerMethodField()
    weeks = serializers.SerializerMethodField()
    class Meta:
        model = Phase
        fields = '__all__'
        list_serializer_class = CustomListSerializer
    def get_totalPrice(self, obj):
        return obj.totalPrice

    def get_weeks(self, obj):
        return obj.period // 7 + (1 if obj.period % 7 > 0 else 0)

    def create(self, validated_data):
        uss_data = validated_data.pop('us_set', [])
        phase = Phase.objects.create(**validated_data)

        for us_data in uss_data:
            us_data.pop('phase', None)
            US.objects.create(phase=phase, **us_data)

        return phase

    def update(self, instance, validated_data):
        uss_data = validated_data.pop('us_set', None)

        # Update base fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Optionnel : gérer mise à jour des US
        if uss_data is not None:
            instance.us_set.all().delete()
            for us_data in uss_data:
                us_data.pop('phase', None)
                US.objects.create(phase=instance, **us_data)

        return instance

class PhaseEtudeSerializer(PhaseSerializer):
    class Meta(PhaseSerializer.Meta):
        model = PhaseEtude
        fields = PhaseSerializer.Meta.fields

    def create(self, validated_data):
        uss_data = validated_data.pop('us_set', [])
        etude = validated_data.pop('etude')

        phase = PhaseEtude.objects.create(etude=etude, **validated_data)

        for us_data in uss_data:
            us_data.pop('phase', None)
            US.objects.create(phase=phase, **us_data)

        return phase

    def update(self, instance, validated_data):
        uss_data = validated_data.pop('us_set', None)

        # Mise à jour de l'`etude` si présente dans la requête
        if 'etude' in validated_data:
            instance.etude = validated_data.pop('etude')

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Synchroniser avec la PhaseMission associée (si elle existe)
        #try:
        #    phase_mission = PhaseMission.objects.get(phaseEtude=instance.id)
        #    # Champs à synchroniser
        #    for field in ['description', 'title', 'methodologie', 'priceJEH', 'beginDate', 'spec', 'period']:
        #        setattr(phase_mission, field, getattr(instance, field))
        #    phase_mission.save()
        #except PhaseMission.DoesNotExist:
        #    pass  # Pas de mission liée, on ne fait rien

        # Gérer les US (on les remplace tous ici, comportement simple)
        if uss_data is not None:
            instance.us_set.all().delete()
            for us_data in uss_data:
                us_data.pop('phase', None)
                US.objects.create(phase=instance, **us_data)

        return instance

class PhaseMissionSerializer(PhaseSerializer):
    phaseEtude = serializers.PrimaryKeyRelatedField(queryset=PhaseEtude.objects.all(), required=False, allow_null=True)

    class Meta(PhaseSerializer.Meta):
        model = PhaseMission
        fields = PhaseSerializer.Meta.fields

    def create(self, validated_data):
        uss_data = validated_data.pop('us_set', [])
        mission = validated_data.pop('mission')

        phase = PhaseMission.objects.create(mission=mission, **validated_data)

        for us_data in uss_data:
            us_data.pop('phase', None)
            US.objects.create(phase=phase, **us_data)

        return phase

    def update(self, instance, validated_data):
        uss_data = validated_data.pop('us_set', None)

        # Mise à jour de la mission si présente dans la requête
        if 'mission' in validated_data:
            instance.mission = validated_data.pop('mission')

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Gérer les US (on les remplace tous ici, comportement simple)
        if uss_data is not None:
            instance.us_set.all().delete()
            for us_data in uss_data:
                us_data.pop('phase', None)
                US.objects.create(phase=instance, **us_data)

        return instance