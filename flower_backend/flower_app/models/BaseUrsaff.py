from django.db import models
from datetime import date
from rest_framework import serializers

class BaseUrsaff(models.Model):
    smic_horaire = models.DecimalField(decimal_places=2, max_digits=5, default=10.0)
    mandat = models.IntegerField(default=2021, primary_key=True) # le mandat EST la primary key.

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