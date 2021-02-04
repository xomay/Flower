from django.db import models
from datetime import date
from rest_framework import serializers
from django.core.validators import MaxValueValidator, MinValueValidator

from flower_app.models.People.Personne import Personne
from flower_app.models.Competence import Competence
from flower_app.models.Etude import Etude

# Commentaire

class RealisateurComment(models.Model):
    content = models.TextField()
    associatedEtude = models.ForeignKey(Etude, on_delete=models.CASCADE) # je n'ai pas mis OneToOne car on peut avoir plusieurs réas pour 1 étude
    date = models.DateField(default=date.today)
    rating = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(0), MaxValueValidator(10)])
    def __str__(self):
        return self.associatedEtude.name + "_"+ str(self.rating)
    

class RealisateurCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RealisateurComment
        fields = '__all__'

# Réalisateur
class Realisateur(Personne):
    promotion = models.IntegerField(default=2021)
    email_insa = models.EmailField(blank=True)
    address = models.CharField(max_length=200)
    postcode = models.CharField(max_length=20)
    town = models.CharField(max_length=60)
    country = models.CharField(max_length=60, default="France")
    nationality = models.CharField(max_length=60, default="FR")
    birth_date = models.DateField()
    birth_place = models.CharField(max_length=60)

    CHOICES_FILIERES = [
        ('INFO','INFO'),
        ('EII', 'EII'),
        ('ECDTI', 'ECDTI'),
        ('SRC', 'SRC'),
        ('GM', 'GM'),
        ('GCU', 'GCU'),
        ('GMA', 'GMA'),
        ('SGM', 'SGM')
    ]

    skills = models.ManyToManyField(Competence, blank=True)
    comments = models.ManyToManyField(RealisateurComment, blank=True)
    security_social_number = models.CharField(max_length=15)
    filiere = models.CharField(max_length=5, choices=CHOICES_FILIERES, default='INFO')

    def __str__(self):
        return self.firstname + ' ' + self.lastname

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
    
    #TODO ajouter un moyen de calculer le nombre d'études.

class RealisateurSerializer(serializers.ModelSerializer):
    rating = serializers.ReadOnlyField()
    etudesAmount = serializers.ReadOnlyField()
    skillsArray = serializers.ReadOnlyField()
    class Meta:
        model = Realisateur
        fields = '__all__'
