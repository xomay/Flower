from django.db import models
from rest_framework import serializers
from flower_app.models.People.Membre import Membre, MembreSerializer
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal
from flower_app.serializers import CustomListSerializer
from flower_app.models.UploadedFile import UploadedFile, UploadedFileSerializer

class NdF(models.Model):
    demandeur = models.ForeignKey(Membre, on_delete=models.RESTRICT)
    mandat = models.IntegerField(default=2021, validators=[MinValueValidator(2020), MaxValueValidator(2100)])
    date = models.DateField()
    objet = models.TextField()
    numberThisYear = models.IntegerField(default=1, validators=[MinValueValidator(0), MaxValueValidator(999)])

    linkedFiles = models.ManyToManyField(UploadedFile, blank=True)

    @property
    def montantHT(self):
        total = Decimal(0)
        for detail in getattr(self, 'ndfdetail_set').all():
            if(detail.isKilometrique):
                total += Decimal(detail.montantTTC)
            else:
                total += Decimal(detail.prixHT)
        return total

    @property
    def montantTVA(self):
        total = Decimal(0)
        for detail in getattr(self, 'ndfdetail_set').all():
            total += Decimal(detail.montantTVA)
        return total

    @property
    def montantTTC(self):
        total = Decimal(0)
        for detail in getattr(self, 'ndfdetail_set').all():
            total += Decimal(detail.montantTTC)
        return total

    @property
    def isKilometrique(self):
        for detail in getattr(self, 'ndfdetail_set').all():
            if(detail.isKilometrique):
                return True
        return False

    def niceMembre(self):
        return self.demandeur.firstname.capitalize()[0] + self.demandeur.lastname.capitalize()[0] # + le numéro

    def niceNumberInYear(self):
        number = self.numberThisYear
        if(number < 10):
            return '00'+str(number)
        elif(number < 100):
            return '0'+str(number)
        return str(number) 

    @property
    def reference(self):
        return str(self.mandat)[-2:] + '-NF' + self.niceNumberInYear() + "-" + self.niceMembre()
        
    def __str__(self):
        return self.reference
    
    class Meta:
       verbose_name = 'Note de Frais'
       verbose_name_plural = 'Notes de Frais'

from flower_app.models.NdFDetail import NdFDetail, NdFDetailSerializer

class NdFSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, write_only=False)
    # Ajout des propeties
    reference = serializers.SerializerMethodField()
    isKilometrique = serializers.SerializerMethodField()
    montantHT = serializers.SerializerMethodField()
    montantTVA = serializers.SerializerMethodField()
    montantTTC = serializers.SerializerMethodField()
    # Re-sérialisation
    demandeur = MembreSerializer(read_only=True)
    details = NdFDetailSerializer(source='ndfdetail_set', many=True)
    linkedFiles = UploadedFileSerializer(many=True, read_only=True)
    class Meta:
        model = NdF
        fields = '__all__'
        list_serializer_class = CustomListSerializer
    def get_reference(self, obj):
        return obj.reference
    def get_isKilometrique(self, obj):
        return obj.isKilometrique
    def get_montantHT(self, obj):
        return obj.montantHT
    def get_montantTVA(self, obj):
        return obj.montantTVA
    def get_montantTTC(self, obj):
        return obj.montantTTC
    
    def create(self, validated_data):
        details = validated_data.get('ndfdetail_set')
        for detail in details:
            detail_instance = NdFDetail(
                ndf=detail['ndf'],
                index=detail['index'],
                description=detail['description'],
                detailType=detail['detailType'],
                prixHT=detail['prixHT'],
                tva=detail['tva'],
                nbKilometres=detail['nbKilometres'],
                prixCentimesKilometres=detail['prixCentimesKilometres'],
                linkedFiles=detail['linkedFiles']
            )
            detail_instance.save()
        if 'ndfdetail_set' in validated_data:
            del validated_data['ndfdetail_set']
        return NdF.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.demandeur = validated_data.get('demandeur', instance.demandeur)
        instance.mandat = validated_data.get('mandat', instance.mandat)
        instance.date = validated_data.get('date', instance.date)
        instance.objet = validated_data.get('objet', instance.objet)
        instance.numberThisYear = validated_data.get('numberThisYear', instance.numberThisYear)
        #instance.linkedFiles.set(validated_data.get('linkedFiles', instance.linkedFiles.all()))
        instance.save()

        details = validated_data.get('ndfdetail_set')
        done = list()

        for detail in details:
            detail_id = detail.get('id', None)
            if detail_id:
                detail_instance = NdFDetail.objects.get(id=detail_id, ndf=instance)
                detail_instance.index = detail.get('index', detail_instance.index)
                detail_instance.description = detail.get('description', detail_instance.description)
                detail_instance.detailType = detail.get('detailType', detail_instance.detailType)

                detail_instance.prixHT = detail.get('prixHT', detail_instance.prixHT)
                detail_instance.tva = detail.get('tva', detail_instance.tva)

                detail_instance.nbKilometres = detail.get('nbKilometres', detail_instance.nbKilometres)
                detail_instance.prixCentimesKilometres = detail.get('prixCentimesKilometres', detail_instance.prixCentimesKilometres)

                detail_instance.ndf = detail.get('ndf', detail_instance.ndf)
                detail_instance.save()
                done.append(detail_id)
            else:
                detail_instance = NdFDetail(
                    ndf=detail['ndf'],
                    index=detail['index'],
                    description=detail['description'],
                    detailType=detail['detailType'],
                    prixHT=detail['prixHT'],
                    tva=detail['tva'],
                    nbKilometres=detail['nbKilometres'],
                    prixCentimesKilometres=detail['prixCentimesKilometres'],
                    linkedFiles=detail['linkedFiles']
                )
                detail_instance.save()
                done.append(detail_instance.id)
        
        for saved_detail in NdFDetail.objects.all().filter(ndf=instance):
            if not saved_detail.id in done:
                saved_detail.delete()

        return instance
