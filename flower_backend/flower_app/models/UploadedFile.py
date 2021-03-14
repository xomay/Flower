from django.db import models
from rest_framework import serializers
from datetime import datetime

from flower_app.models.People.Membre import Membre
from django.contrib import admin
from django.contrib.auth.models import Group

class UploadedFile(models.Model):
    #Membre qui upload le fichier
    author = models.ForeignKey(Membre, on_delete=models.RESTRICT)
    # Nom à afficher
    displayName = models.CharField(max_length=60)
    # Date de l'upload
    uploadDate = models.DateTimeField(auto_now=True)
    # Permissions nécessaires pour lire le fichier
    permissions = models.ManyToManyField(Group, blank=True)
    # Fichier en lui-même
    data = models.FileField(upload_to='uploads/')

    def __str__(self):
        return "["+self.uploadDate.date().strftime("%d/%m/%Y") + " " + self.uploadDate.time().strftime("%H:%M:%S")+"] " + self.displayName

class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = '__all__'
