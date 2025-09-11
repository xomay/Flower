from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

from rest_framework import serializers

from flower_app.models.People.Membre import Membre
from flower_app.models.People.Personne import Personne
from flower_app.models.Competence import Competence
from flower_app.models.Etude import Etude

from datetime import date

# Commentaire

class RealisateurComment(models.Model):
    content = models.TextField()
    associatedEtude = models.ForeignKey(Etude, on_delete=models.CASCADE) # je n'ai pas mis OneToOne car on peut avoir plusieurs réas pour 1 étude
    date = models.DateField(default=date.today)
    rating = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(0), MaxValueValidator(10)])
    def __str__(self):
        return self.associatedEtude.name + "_"+ str(self.rating)

    def anonymiser(self):
        self.content = settings.ANONYMISATION_STRING
        self.save()
    

class RealisateurCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RealisateurComment
        fields = '__all__'

# Réalisateur
class Realisateur(Personne):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    promotion = models.IntegerField(default=2021)
    email_insa = models.EmailField(blank=True)
    address = models.CharField(max_length=200)
    postcode = models.CharField(max_length=20)
    town = models.CharField(max_length=60)
    country = models.CharField(max_length=60, default="France")
    nationality = models.CharField(max_length=60, default="FR")
    birth_date = models.DateField()
    birth_place = models.CharField(max_length=60)
    ba = models.DateField(null=True)
    ba_id = models.IntegerField(null=True)
    CHOICES_FILIERES = [
        ('INFO','INFO'),
        ('EII', 'EII'),
        ('E&T', 'E&T'),
        ('MA', 'MA'),
        ('GCU', 'GCU'),
        ('GMA', 'GMA'),
        ('GPM', 'GPM'),
        ('STPI', 'STPI')
    ]
    isMember = models.BooleanField(default=False)
    member = models.ForeignKey(Membre, on_delete=models.CASCADE, null=True, blank=True)

    skills = models.ManyToManyField(Competence, blank=True)
    comments = models.ManyToManyField(RealisateurComment, blank=True)
    security_social_number = models.CharField(max_length=15)
    filiere = models.CharField(max_length=5, choices=CHOICES_FILIERES, default='INFO')
    
    
    def __str__(self):
        return self.firstname + ' ' + self.lastname

    def anonymiser(self):
        super().anonymiser()
        self.postcode = settings.ANONYMISATION_STRING
        self.promotion = settings.ANONYMISATION_INTEGER
        self.address = settings.ANONYMISATION_STRING
        self.email_insa = settings.ANONYMISATION_STRING
        self.birth_date = settings.ANONYMISATION_DATE
        self.birth_place = settings.ANONYMISATION_STRING
        self.security_social_number = settings.ANONYMISATION_STRING
        self.filiere = settings.ANONYMISATION_STRING
        self.town = settings.ANONYMISATION_STRING
        self.country = settings.ANONYMISATION_STRING
        self.nationality = settings.ANONYMISATION_STRING
        for elt in self.comments.all():
            elt.anonymiser()
        self.save()


    @property
    def rating(self):
        if(len(self.comments.all()) == 0):
            return -1
        rate = 0
        for comment in self.comments.all():
            rate += comment.rating
        return rate / len(self.comments.all())
    
    @property
    def etudesAmount(self):
        return len(self.comments.all())
        
    @property
    def skillsArray(self):
        skillsArr = []
        for skill in self.skills.all():
            skillsArr.append(str(skill))
        return skillsArr

    @property
    def ref_ba(self):
        if self.isMember:
            ref_ba = str(self.ba.year % 100) + 'C' + '%03d' % self.ba_id
            return ref_ba
        else:
            ref_ba = str(self.ba.year % 100) + 'R' + '%03d' % self.ba_id
            return ref_ba
    
    #TODO ajouter un moyen de calculer le nombre d'études.

class RealisateurSerializer(serializers.ModelSerializer):
    rating = serializers.ReadOnlyField()
    etudesAmount = serializers.ReadOnlyField()
    skillsArray = serializers.ReadOnlyField()
    ref_ba = serializers.ReadOnlyField()

    # On ne veut pas plusieurs comments pour même réa et même étude.
    def update(self, instance, validated_data):
        passed = list()
        for comment in validated_data['comments']:
            if(comment.associatedEtude.id in passed):
                raise ValidationError("Cannot accept more than 1 comment for 1 Etude & 1 Realisateur.")
            passed.append(comment.associatedEtude.id)
        return super().update(instance, validated_data)

    class Meta:
        model = Realisateur
        fields = '__all__'
