from django.db import models
from rest_framework import serializers

from flower_app.models.Etude import Etude
from flower_app.serializers import CustomListSerializer


class Requirement(models.Model):
    reference = models.CharField(max_length=50, default='REF')
    description = models.TextField()
    etude = models.ForeignKey(Etude, on_delete=models.CASCADE, related_name='requirements')

    def __str__(self):
        return self.reference

    @property
    def phases(self):
        from .GroupePhase import PhaseEtude
        phases = PhaseEtude.objects.filter(requirements__id=self.id)
        return [phase.index for phase in phases]

class RequirementSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, write_only=False)
    phases = serializers.ListField(child=serializers.IntegerField(), required=False)
    class Meta:
        model = Requirement
        fields = '__all__'
        list_serializer_class = CustomListSerializer

    def update(self, instance, validated_data):
        phases = validated_data.pop('phases', None)
        print("Update Requirement", validated_data, instance)
        instance = super().update(instance, validated_data)
        if phases is not None:
            from .GroupePhase import PhaseEtude
            for p in (PhaseEtude.objects.filter(etude=instance.etude, requirements=instance)
                    .exclude(index__in=phases)):
                p.requirements.remove(instance)
            for phase in phases:
                print("Phase ", phase)
                phase_instance = PhaseEtude.objects.get(index=phase, etude=instance.etude, state='ACTIVE')
                phase_instance.requirements.add(instance)
        return instance