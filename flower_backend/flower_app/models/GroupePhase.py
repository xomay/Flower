from django.db import models
from django.db.models.deletion import RESTRICT
from rest_framework import serializers
from ..serializers import CustomListSerializer
from datetime import date, timedelta

POSSIBILITIES_ATTR = ['etude_set', 'avenant_set']
class GroupesSet(models.Model):
    # depuis étude / avenant, on le récupère
    def __str__(self):
        for attr in POSSIBILITIES_ATTR:
            if hasattr(self, attr):
                coll = getattr(self, attr)
                if coll.count() > 0:
                    return "GS("+str(coll.first())+")"
        return "GS_(UNDEFINED)"

class Groupe(models.Model):
    title = models.CharField(max_length=60)
    index = models.IntegerField()
    description = models.TextField()

    owner = models.ForeignKey(GroupesSet, on_delete=models.RESTRICT, null=True)

    def __str__(self):
        return self.owner.__str__() + " > " + self.title

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
    methodologie = models.TextField(blank=True, default='')

    beginDate = models.DateField(default=date.today)
    period = models.IntegerField(default=14)
    
    nbJEH = models.IntegerField(default=1)
    priceJEH = models.DecimalField(default=400, max_digits=10, decimal_places=2)

    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)

    def __str__(self):
        return self.groupe.__str__() + " > " + self.title

    @property
    def totalPrice(self):
        return self.nbJEH * self.priceJEH
    
    @property
    def finishDate(self):
        return (self.beginDate + timedelta(days=self.period)).isoformat()

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
    uss = USSerializer(source='us_set', many=True)
    finishDate = serializers.SerializerMethodField()
    totalPrice = serializers.SerializerMethodField()
    class Meta:
        model = Phase
        fields = '__all__'
        list_serializer_class = CustomListSerializer
    def get_finishDate(self, obj):
        return obj.finishDate
    def get_totalPrice(self, obj):
        return obj.totalPrice

    def create(self, validated_data):
        if 'us_set' in validated_data:
            del validated_data['us_set']
        return Phase.objects.create(**validated_data)


class GroupeSerializerBasic(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Groupe

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
        instance.owner = validated_data.get('owner', instance.owner)
        instance.save()

        phases = validated_data.get('phase_set')
        for phase in phases:
            phase_id = phase.get('id', None)
            if phase_id:
                phase_instance = Phase.objects.get(id=phase_id, groupe=instance)
                phase_instance.title = phase.get('title', phase_instance.title)
                phase_instance.index = phase.get('index', phase_instance.index)
                phase_instance.description = phase.get('description', phase_instance.description)
                phase_instance.methodologie = phase.get('methodologie', phase_instance.methodologie)

                phase_instance.beginDate = phase.get('beginDate', phase_instance.beginDate)
                phase_instance.period = phase.get('period', phase_instance.period)

                phase_instance.nbJEH = phase.get('nbJEH', phase_instance.nbJEH)
                phase_instance.priceJEH = phase.get('priceJEH', phase_instance.priceJEH)

                phase_instance.groupe = phase.get('groupe', phase_instance.groupe)
                phase_instance.save()

                uss = phase.get('us_set')
                for us in uss:
                    us_id = us.get('id', None)
                    us_instance = US.objects.get(id=us_id, phase=phase_instance)
                    us_instance.name = us.get('name', us_instance.name)
                    us_instance.state = us.get('state', us_instance.name)
                    us_instance.save()

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

class GroupesSetSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, write_only=False)
    groupes = GroupeDetailSerializer(source='groupe_set', many=True, read_only=True)
    class Meta:
        model = GroupesSet
        fields = '__all__'
