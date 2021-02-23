from django.db import models
from rest_framework import serializers
from flower_app.models.NdF import NdF

class NdFDetail(models.Model):
    ndf = models.ForeignKey(NdF, on_delete=models.RESTRICT)
    index = models.IntegerField()
    description = models.TextField()

    TYPES_DETAILS = [
      ('N', 'Normale'),
      ('K', 'Kilométrique')
    ]
    detailType = models.CharField(max_length=1, choices=TYPES_DETAILS, default='N')

    # NF normale
    prixHT = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    tva = models.DecimalField(decimal_places=2, max_digits=5, default=0.2)

    # NF kilométrique
    nbKilometres = models.IntegerField(default=0)
    prixCentimesKilometres = models.IntegerField(default=6)

    def __str__(self):
        return '[Détail](' + self.ndf.reference + ')[' + str(self.index) + ']'

    @property
    def isKilometrique(self):
        return self.detailType == 'K'

    @property
    def montantTVA(self):
        return self.tva * self.prixHT

    @property
    def montantTTC(self):
        if(self.isKilometrique):
            return self.nbKilometres * self.prixCentimesKilometres
        return self.prixHT + self.montantTVA

    class Meta:
       verbose_name = 'Note de Frais (détails)'
       verbose_name_plural = 'Notes de Frais (détails)'

class NdFDetailSerializer(serializers.ModelSerializer):
    isKilometrique = serializers.SerializerMethodField()
    montantTVA = serializers.SerializerMethodField()
    montantTTC = serializers.SerializerMethodField()
    class Meta:
        model = NdFDetail
        fields = '__all__'
    def get_isKilometrique(self, obj):
        return obj.isKilometrique
    def get_montantTVA(self, obj):
        return obj.montantTVA
    def get_montantTTC(self, obj):
        return obj.montantTTC
