from django.db import models
from rest_framework import serializers

from flower_app.models.Etude import Etude
from flower_app.models.People.Prospect import Prospect

# Create your models here.
class Facture(models.Model):

    project = models.ForeignKey(Etude, on_delete=models.RESTRICT)
    accountingPeriod = models.IntegerField(default=2020)
    payee = models.ForeignKey(Prospect, on_delete=models.RESTRICT)
    invoiceNumber = models.IntegerField()
    
    INVOICE_CHOICES = [
      ('FA', 'Facture d\'achat'),
      ('FVA', 'Facture d\'acompte'),
      ('FVS', 'Facture de solde')
    ]
    invoiceType = models.CharField(max_length=3, choices=INVOICE_CHOICES)
    issueDate = models.DateField()
    paymentDate = models.DateField(blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return 'Facture'

    @property
    def reference(self):
        return self.invoiceType + '_' + str(self.invoiceNumber)

    @property
    def amountTaxes(self):
        total = 0
        for detail in self.facturedetail_set.iterator():
            total += detail.taxesAmount
        return total

    @property
    def amountWithoutTaxes(self):
        total = 0
        for detail in self.facturedetail_set.iterator():
            total += detail.taxFreeAmount
        return total

    @property
    def totalToPay(self):
        return self.amountWithoutTaxes + self.amountTaxes

from flower_app.models.FactureDetail import FactureDetailSerializer

class FactureSerializer(serializers.ModelSerializer):
    details = FactureDetailSerializer(source='facturedetail_set', many=True, read_only=True)
    class Meta:
        model = Facture
        fields = '__all__'
