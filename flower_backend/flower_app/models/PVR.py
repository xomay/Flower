from django.db import models
from rest_framework import serializers

from flower_app.models.Etude import Etude
from flower_app.models.People.Membre import Membre
from flower_app.models.People.Employe import Employe

# Create your models here.
class PVR(models.Model):
    project = models.ForeignKey(Etude, on_delete=models.RESTRICT)
    signer1 = models.ForeignKey(Membre, on_delete=models.RESTRICT)
    signer2 = models.ForeignKey(Employe, on_delete=models.RESTRICT)

    PVR_CHOICES = [
      ('I', 'Intermédiaire'),
      ('F', 'Finale')
    ]
    documentType = models.CharField(max_length=1, choices=PVR_CHOICES)
    signingDate = models.DateField()
    deliverable = models.TextField()

    def __str__(self):
        return self.reference

    @property
    def documentName(self):
      return 'Procès Verbal de Recette ' + ('Intermédiaire' if self.documentType == 'I' else 'Finale')

    @property
    def reference(self):
        return 'PV' + ('I' if self.documentType == 'I' else '' + '_') + str(self.project.number)

class PVRSerializer(serializers.ModelSerializer):
    class Meta:
        model = PVR
        fields = '__all__'
