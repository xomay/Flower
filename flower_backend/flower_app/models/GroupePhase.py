from django.db import models
from rest_framework import serializers

from flower_app.models.Etude import Etude
from flower_app.serializers import CustomListSerializer

from datetime import date, timedelta

class Groupe(models.Model):
    title = models.CharField(max_length=60)
    index = models.IntegerField()
    description = models.TextField()

    project = models.ForeignKey(Etude, on_delete=models.RESTRICT)

    def __str__(self):
        return self.title

    @property
    def nbJEH(self):
        total = 0
        for phase in self.phase_set.iterator():
            total += phase.nbJEH
        return total

    @property
    def totalPrice(self):
        total = 0
        for phase in self.phase_set.iterator():
            total += phase.totalPrice
        return total

class Phase(models.Model):
    title = models.CharField(max_length=200, default='Titre')
    index = models.IntegerField()
    description = models.TextField(default='')
    goals = models.TextField(default='')

    beginDate = models.DateField(default=date.today)
    period = models.IntegerField(default=14)
    
    nbJEH = models.IntegerField(default=1)
    priceJEH = models.DecimalField(default=400, max_digits=10, decimal_places=2)

    groupe = models.ForeignKey(Groupe, on_delete=models.RESTRICT)

    def __str__(self):
        return self.title

    @property
    def totalPrice(self):
        return self.nbJEH * self.priceJEH
    
    @property
    def finishDate(self):
        return (date.fromisoformat(str(self.beginDate)) + timedelta(days=self.period)).isoformat()

class PhaseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, write_only=False)
    class Meta:
        model = Phase
        fields = '__all__'
        list_serializer_class = CustomListSerializer

class GroupeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, write_only=False)
    phases = PhaseSerializer(source='phase_set', many=True)

    def create(self, validated_data):
        if 'phase_set' in validated_data:
            del validated_data['phase_set']
        return Groupe.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.index = validated_data.get('index', instance.index)
        instance.description = validated_data.get('description', instance.description)
        instance.project = validated_data.get('project', instance.project)
        instance.save()

        phases = validated_data.get('phase_set')
        for phase in phases:
            phase_id = phase.get('id', None)
            if phase_id:
                phase_instance = Phase.objects.get(id=phase_id, groupe=instance)
                phase_instance.title = phase.get('title', phase_instance.title)
                phase_instance.index = phase.get('index', phase_instance.index)
                phase_instance.description = phase.get('description', phase_instance.description)
                phase_instance.goals = phase.get('goals', phase_instance.goals)

                phase_instance.beginDate = phase.get('beginDate', phase_instance.beginDate)
                phase_instance.period = phase.get('period', phase_instance.period)
                
                phase_instance.nbJEH = phase.get('nbJEH', phase_instance.nbJEH)
                phase_instance.priceJEH = phase.get('priceJEH', phase_instance.priceJEH)

                phase_instance.groupe = phase.get('groupe', phase_instance.groupe)
                phase_instance.save()

        return instance

    class Meta:
        model = Groupe
        fields = '__all__'
        list_serializer_class = CustomListSerializer

class GroupeDetailSerializer(serializers.ModelSerializer):
    phases = PhaseSerializer(source='phase_set', many=True)
    class Meta:
        model = Groupe
        fields = '__all__'
