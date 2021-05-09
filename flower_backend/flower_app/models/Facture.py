from django.db import models
from rest_framework import serializers

from flower_app.models.Etude import Etude
from flower_app.models.People.Prospect import Prospect

# Create your models here.
class Facture(models.Model):
    project = models.ForeignKey(Etude, on_delete=models.RESTRICT)
    accountingPeriod = models.IntegerField(default=2020)
    payee = models.ForeignKey(Prospect, on_delete=models.RESTRICT)
    invoiceNumber = models.CharField(max_length=20)

    INVOICE_CHOICES = [
        ('FA', 'Facture d\'achat'),
        ('FVA', 'Facture d\'acompte'),
        ('FVI', 'Facture intermédiaire'),
        ('FVS', 'Facture de solde')
    ]
    invoiceType = models.CharField(max_length=3, choices=INVOICE_CHOICES)
    issueDate = models.DateField()
    paymentDate = models.DateField(blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return self.description

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

from flower_app.models.FactureDetail import FactureDetailSerializer, FactureDetail

class FactureSerializer(serializers.ModelSerializer):
    details = FactureDetailSerializer(source='facturedetail_set', many=True, read_only=True)
    # Ajout des propreties
    reference = serializers.SerializerMethodField()
    amountTaxes = serializers.SerializerMethodField()
    amountWithoutTaxes = serializers.SerializerMethodField()
    totalToPay = serializers.SerializerMethodField()
    def get_reference(self, obj):
        return obj.reference
    def get_amountTaxes(self, obj):
        return obj.amountTaxes
    def get_amountWithoutTaxes(self, obj):
        return obj.amountWithoutTaxes
    def get_totalToPay(self, obj):
        return obj.totalToPay
    
    def create(self, validated_data):
        instance = Facture.objects.create(**validated_data)
        details = self.initial_data.get('details')
        for detail in details:
            description = detail.get('description')
            taxFreeAmount = detail.get('taxFreeAmount')
            taxes = detail.get('taxes')
            FactureDetail.objects.create(invoice=instance, description=description, taxFreeAmount=taxFreeAmount, taxes=taxes)
        return instance

    def update(self, instance, validated_data):
        instance.project = validated_data.get('project', instance.project)
        instance.accountingPeriod = validated_data.get('accountingPeriod', instance.accountingPeriod)
        instance.payee = validated_data.get('payee', instance.payee)
        instance.invoiceNumber = validated_data.get('invoiceNumber', instance.invoiceNumber)

        instance.invoiceType = validated_data.get('invoiceType', instance.invoiceType)
        instance.issueDate = validated_data.get('issueDate', instance.issueDate)
        instance.paymentDate = validated_data.get('paymentDate', instance.paymentDate)
        instance.description = validated_data.get('description', instance.description)

        instance.save()

        details = self.initial_data.get('details')
        for detail in details:
            detail_id = detail.get('id', None)
            if detail_id: # Si le détail existe déjà
                detail_instance = FactureDetail.objects.get(id=detail_id, invoice=instance)
                detail_instance.description = detail.get('description', detail_instance.description)
                detail_instance.taxFreeAmount = detail.get('taxFreeAmount', detail_instance.taxFreeAmount)
                detail_instance.taxes = detail.get('taxes', detail_instance.taxes)
                detail_instance.invoice = instance

                detail_instance.save()
            else: # si on l'a encore jamais créé
                print(detail)
                description = detail['description']
                taxFreeAmount = detail['taxFreeAmount']
                taxes = detail['taxes']
                FactureDetail.objects.create(invoice=instance, description=description, taxFreeAmount=taxFreeAmount, taxes=taxes)

        return instance

    class Meta:
        model = Facture
        fields = '__all__'
