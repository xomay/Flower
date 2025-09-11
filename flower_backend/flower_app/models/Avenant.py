from django.db import models
from django.db.models.deletion import RESTRICT
from rest_framework import serializers

from ..serializers import CustomListSerializer


class Avenant(models.Model):
    index = models.IntegerField(default=0)
    description = models.TextField(default='', blank=True, null=True)

    is_delai = models.BooleanField(default=False)
    is_cdc = models.BooleanField(default=False)
    is_budget = models.BooleanField(default=False)
    is_methodo = models.BooleanField(default=False)

    #Champ pour préciser des éléments tel que des modifications hors flower par exemple
    additional = models.TextField(default='', blank=True, null=True)

    def __str__(self):
        return self.description


class AvenantEtude(Avenant):
    from .Etude import Etude
    from .DocEtude import DocEtude, DocMission, CEDetailSerializer
    etude = models.ForeignKey(Etude, on_delete=models.RESTRICT, related_name='avenantsEtude')
    doc_etude = models.ForeignKey(DocEtude, on_delete=models.CASCADE, blank=True, null=True)


class AvenantMission(Avenant):
    from .Mission import Mission
    from .DocEtude import DocEtude, DocMission, CEDetailSerializer
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name='avenantsMission')
    doc_mission = models.ForeignKey(DocMission, on_delete=models.RESTRICT, blank=True, null=True)
    avenant_etude = models.ForeignKey(AvenantEtude, on_delete=models.CASCADE, related_name='avenantEtudeAssociate', null=True)


class AvenantSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    phases = serializers.SerializerMethodField()

    class Meta:
        model = Avenant
        fields = '__all__'
        list_serializer_class = CustomListSerializer

    def get_phases(self, instance):
        from .GroupePhase import PhaseSerializer
        return PhaseSerializer(instance.avenantCreator.all(), many=True).data

    def create(self, validated_data):
        avenant = Avenant.objects.create(**validated_data)
        return avenant

    def update(self, instance, validated_data):
        # Update base fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class AvenantEtudeSerializer(AvenantSerializer):
    ref = serializers.SerializerMethodField()

    class Meta:
        model = AvenantEtude
        fields = '__all__'
        list_serializer_class = CustomListSerializer

    def get_ref(self, instance):
        ref = ""
        if instance.etude.cc:
            ref = "BCR"
        else:
            ref = "AV"
        ref = ref + str(instance.index) + "-"
        if instance.is_delai:
            ref = ref + "D,"
        if instance.is_methodo:
            ref = ref + "M,"
        if instance.is_cdc:
            ref = ref + "C,"
        if instance.is_budget:
            ref = ref + "B,"
        ref = ref[:-1] + "_" + str(instance.etude.number)

        return ref

    def create(self, validated_data):
        etude = validated_data.pop('etude')

        avenant = AvenantEtude.objects.create(etude=etude, **validated_data)

        return avenant

class AvenantEtudeDetailSerializer(AvenantSerializer):
    from .DocEtude import DocEtude, DocMission, CEDetailSerializer

    ref = serializers.SerializerMethodField()
    doc_etude = CEDetailSerializer(read_only=True)

    class Meta:
        model = AvenantEtude
        fields = '__all__'
        list_serializer_class = CustomListSerializer

    def get_ref(self, instance):
        ref = ""
        if instance.etude.cc:
            ref = "BCR"
        else:
            ref = "AV"
        ref = ref + str(instance.index) + "-"
        if instance.is_delai:
            ref = ref + "D,"
        if instance.is_methodo:
            ref = ref + "M,"
        if instance.is_cdc:
            ref = ref + "C,"
        if instance.is_budget:
            ref = ref + "B,"
        ref = ref[:-1] + "_" + str(instance.etude.number)

        return ref


class AvenantMissionSerializer(AvenantSerializer):
    ref = serializers.SerializerMethodField()

    class Meta:
        model = AvenantMission
        fields = '__all__'
        list_serializer_class = CustomListSerializer

    def get_ref(self, instance):
        ref = "AVRM" + str(instance.index) + "-"
        if instance.is_delai:
            ref = ref + "D,"
        if instance.is_methodo:
            ref = ref + "M,"
        if instance.is_cdc:
            ref = ref + "C,"
        if instance.is_budget:
            ref = ref + "B,"
        ref = ref[:-1] + "_" + str(instance.mission.project.number)

        return ref

    def create(self, validated_data):
        mission = validated_data.pop('mission')

        avenant = AvenantMission.objects.create(mission=mission, **validated_data)

        return avenant

class AvenantMissionDetailSerializer(AvenantSerializer):
    from .DocEtude import DocMissionSerializer

    ref = serializers.SerializerMethodField()
    doc_mission = DocMissionSerializer(read_only=True)

    class Meta:
        model = AvenantMission
        fields = '__all__'
        list_serializer_class = CustomListSerializer

    def get_ref(self, instance):
        ref = "AVRM" + str(instance.index) + "-"
        if instance.is_delai:
            ref = ref + "D,"
        if instance.is_methodo:
            ref = ref + "M,"
        if instance.is_cdc:
            ref = ref + "C,"
        if instance.is_budget:
            ref = ref + "B,"
        ref = ref[:-1] + "_" + str(instance.mission.project.number)

        return ref