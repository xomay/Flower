from django.db import models
from django.core.exceptions import ValidationError
from rest_framework import serializers

class ParamsJE(models.Model):
    # Nom de la Junior Entreprise.
    je_name = models.CharField(max_length=50)
    # Abrévation de la Junior Entreprise
    je_abbrevation = models.CharField(max_length=20)
    # Addresse postale
    je_address = models.CharField(max_length=120)
    # Url du site web
    je_url = models.CharField(max_length=80)
    # email de contact
    je_contact = models.CharField(max_length=40)
    # suffixe des élèves de l'école (sans le '@')
    mail_suffix = models.CharField(max_length=40)

    # Président : prénom
    president_firstname = models.CharField(max_length=40)
    # Président : nom
    president_lastname = models.CharField(max_length=40)
    # Président : texte
    president_text = models.CharField(max_length=40)
    # Trésorier : prénom
    treso_firstname = models.CharField(max_length=40)
    # Trésorier : nom
    treso_lastname = models.CharField(max_length=40)
    # Trésorier : texte
    treso_text = models.CharField(max_length=40)

    # Taux de TVA (20% = 0.2)
    global_tva = models.DecimalField(decimal_places=2, max_digits=3, default=0.2)
    # Frais de dossier
    global_frais = models.DecimalField(decimal_places=2, max_digits=10, default=90)
    # Pourcentage compte par défault
    global_accompte = models.DecimalField(decimal_places=2, max_digits=10, default=0.3)

    # Année d'utilisation de Flower
    je_startFlower = models.IntegerField(default=2021)
    
    def __str__(self):
        return "PARAMS_JE: " + self.je_name

    class Meta: # Affichage custom dans l'onglet d'administration
       verbose_name = 'Paramètres JE'
       verbose_name_plural = 'Paramètres JE'

    # On ne veut que une instance de paramètres.
    def save(self, *args, **kwargs):
        if not self.pk and ParamsJE.objects.exists():
            raise ValidationError("Il ne peut il y avoir qu'une instance de ParamsJe.")
        self.id = 1
        return super(ParamsJE, self).save(*args, **kwargs)

class ParamsJESerializer(serializers.ModelSerializer):
    class Meta:
        model = ParamsJE
        fields = '__all__'