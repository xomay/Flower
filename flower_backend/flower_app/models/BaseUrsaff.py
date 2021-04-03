from django.db import models
from datetime import date
from rest_framework import serializers

class BaseUrsaff(models.Model):
    # Mandat (primary key)
    mandat = models.IntegerField(default=2021, primary_key=True)
    # Smic horaire de cette année
    smic_horaire = models.DecimalField(decimal_places=2, max_digits=5, default=10.0)
    # Différents taux de cotisation pour la JUNIOR cette année.
    taux_junior_sante = models.DecimalField(decimal_places=6, max_digits=8, default=0.13)
    taux_junior_accidents = models.DecimalField(decimal_places=6, max_digits=8, default=0.01)
    taux_junior_retraite_1 = models.DecimalField(decimal_places=6, max_digits=8, default=0.0855)
    taux_junior_retraite_2 = models.DecimalField(decimal_places=6, max_digits=8, default=0.019)
    taux_junior_famille = models.DecimalField(decimal_places=6, max_digits=8, default=0.0525)
    taux_junior_chomage = models.DecimalField(decimal_places=6, max_digits=8, default=0.042)
    taux_junior_autres = models.DecimalField(decimal_places=6, max_digits=8, default=0.00416)
    taux_junior_csg = models.DecimalField(decimal_places=6, max_digits=8, default=0.0)
    taux_junior_csgcrds = models.DecimalField(decimal_places=6, max_digits=8, default=0.0)
    taux_junior_exonerations = models.DecimalField(decimal_places=6, max_digits=8, default=0.0)
    # Différents taux de cotisation pour les RÉAS cette année.
    taux_realisateur_sante = models.DecimalField(decimal_places=6, max_digits=8, default=0.0)
    taux_realisateur_accidents = models.DecimalField(decimal_places=6, max_digits=8, default=0.0)
    taux_realisateur_retraite_1 = models.DecimalField(decimal_places=6, max_digits=8, default=0.069)
    taux_realisateur_retraite_2 = models.DecimalField(decimal_places=6, max_digits=8, default=0.004)
    taux_realisateur_famille = models.DecimalField(decimal_places=6, max_digits=8, default=0.0)
    taux_realisateur_chomage = models.DecimalField(decimal_places=6, max_digits=8, default=0.0)
    taux_realisateur_autres = models.DecimalField(decimal_places=6, max_digits=8, default=0.0)
    taux_realisateur_csg = models.DecimalField(decimal_places=6, max_digits=8, default=0.068)
    taux_realisateur_csgcrds = models.DecimalField(decimal_places=6, max_digits=8, default=0.029)
    taux_realisateur_exonerations = models.DecimalField(decimal_places=6, max_digits=8, default=0.0)

    @property
    def baseValue(self):
        return 4 * self.smic_horaire

    def __str__(self):
        return "Base URSAFF ("+str(self.mandat)+") : " + str(self.baseValue)

class BaseUrsaffSerializer(serializers.ModelSerializer):
    baseValue = serializers.ReadOnlyField()
    class Meta:
        model = BaseUrsaff
        fields = '__all__'
        
def getLastBase():
    return BaseUrsaff.objects.all().order_by('-mandat')[0]