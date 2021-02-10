from django.db import models
from rest_framework import serializers

from flower_app.models.Facture import Facture

# Create your models here.
class FactureDetail(models.Model):
    invoice = models.ForeignKey(Facture, on_delete=models.CASCADE)
    description = models.TextField()
    taxFreeAmount = models.DecimalField(decimal_places=2, max_digits=10)
    taxes = models.DecimalField(decimal_places=2, default=0.2,max_digits=10)

    def __str__(self):
        return 'Facture detail - ' + self.description

    @property
    def taxesAmount(self):
      return self.taxFreeAmount * self.taxes

    @property
    def totalAmount(self):
      return self.taxFreeAmount * (1 + self.taxes)

class FactureDetailSerializer(serializers.ModelSerializer):
    taxesAmount = serializers.ReadOnlyField()
    totalAmount = serializers.ReadOnlyField()

    class Meta:
        model = FactureDetail
        fields = '__all__'
