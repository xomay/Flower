from django.db import models
from django.dispatch import receiver
from rest_framework import serializers
from datetime import datetime
import os
from flower_app.models.People.Membre import Membre, MembreSerializer
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

@receiver(models.signals.post_delete, sender=UploadedFile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.data:
        if os.path.isfile(instance.data.path):
            os.remove(instance.data.path)

class UploadedFileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, write_only=False)
    author = MembreSerializer(read_only=True)
    uploadDate = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()
    class Meta:
        model = UploadedFile
        fields = ('id', 'author','displayName','uploadDate','permissions','size')
    def get_uploadDate(self, obj):
        return obj.uploadDate.date().strftime("%d/%m/%Y") + " " + obj.uploadDate.time().strftime("%H:%M:%S")
    def get_size(self, obj):
        return obj.data.size
