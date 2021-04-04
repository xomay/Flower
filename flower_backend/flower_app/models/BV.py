from django.db import models
from rest_framework import serializers

from flower_app.models.Mission import Mission, MissionSerializer
from flower_app.models.BaseUrsaff import getLastBase

# Classe spécialisée, juste pour stocker les valeurs des cotisations xd
class Cotisation(models.Model):
    montant_base = models.DecimalField(decimal_places=6, max_digits=8)
    taux_junior = models.DecimalField(decimal_places=6, max_digits=8)
    taux_realisateur = models.DecimalField(decimal_places=6, max_digits=8)

    @property
    def montant_junior(self):
        return self.montant_base * self.taux_junior
    @property
    def montant_realisateur(self):
        return self.montant_base * self.taux_realisateur

    def to_json(self):
        return {
            'montant_base' : self.montant_base,
            'taux_junior' : self.taux_junior,
            'montant_junior' : self.montant_junior,
            'taux_realisateur' : self.taux_realisateur,
            'montant_realisateur' : self.montant_realisateur
        }

class CotisationSerializer(serializers.ModelSerializer):
    montant_junior = serializers.ReadOnlyField()
    montant_realisateur = serializers.ReadOnlyField()
    class Meta:
        model = Cotisation
        fields = '__all__'

# BV en tant que tel. Comme le python c'est de la daube on est obligé de mettre la dépendance au dessus.
class BV(models.Model):
    # Informations globales
    rdm = models.ForeignKey(Mission, on_delete=models.RESTRICT)
    reference = models.CharField(max_length=40) # Référence dans la JE (genre BV_XXX)
    reference_nationale = models.CharField(max_length=40) # Référence pour l'état (suite de caractètes sans queue ni tête)
    date = models.DateField()
    versement_mode = models.CharField(max_length=10, choices=[
      ('Virement', 'Virement'),
      ('Chèque', 'Chèque'),
      ('Espèces', 'Espèces'), # Le mode 'espèce' est là pour faire joli :D
      ('Autre', 'Autre')
    ])
    # Cotisations. bon ba c'est pas marrant du tout, mais c'est parti quand même xD
    coti_sante = models.ForeignKey(Cotisation, on_delete=models.RESTRICT, related_name="coti_sante")
    coti_accidents = models.ForeignKey(Cotisation, on_delete=models.RESTRICT, related_name="coti_accidents")
    coti_retraite_1 = models.ForeignKey(Cotisation, on_delete=models.RESTRICT, related_name="coti_retraite_1")
    coti_retraite_2 = models.ForeignKey(Cotisation, on_delete=models.RESTRICT, related_name="coti_retraite_2")
    coti_famille = models.ForeignKey(Cotisation, on_delete=models.RESTRICT, related_name="coti_famille")
    coti_chomage = models.ForeignKey(Cotisation, on_delete=models.RESTRICT, related_name="coti_chomage")     # chomage : seule cotisation indexée sur rémunération brute
    coti_autres = models.ForeignKey(Cotisation, on_delete=models.RESTRICT, related_name="coti_autres")
    coti_csg = models.ForeignKey(Cotisation, on_delete=models.RESTRICT, related_name="coti_csg")
    coti_csgcrds = models.ForeignKey(Cotisation, on_delete=models.RESTRICT, related_name="coti_csgcrds")
    coti_exonerations = models.ForeignKey(Cotisation, on_delete=models.RESTRICT, related_name="coti_exonerations")

    # Ces quatre taux là servent à effectuer un calcul sur l' "évolution de la rémunération liée à la suppression des cotisations chômage et maladie" du montant net.
    # Bref du coup c'est un peu mystérieux, et je laisse modifiable un peu par principe xd
    taux_sccm_1 = models.DecimalField(decimal_places=5, max_digits=10, default=0.0075)
    taux_sccm_2 = models.DecimalField(decimal_places=5, max_digits=10, default=-0.017)
    taux_sccm_3 = models.DecimalField(decimal_places=5, max_digits=10, default=0.0095)
    taux_sccm_4 = models.DecimalField(decimal_places=5, max_digits=10, default=0.0145)
    # Champ toujours nul à Ouest INSA. On sait pas si c'est le cas ailleurs, donc go le laisser en truc modifiable
    # NOTE : c'est utilisé nulle part car je sais pas DU TOUT à quoi ça sert. Déposez une issue si vous savez ! :D
    allegement_de_cotisations_junior = models.DecimalField(decimal_places=5, max_digits=10, default=0)

    def __str__(self):
        return 'BV '+self.reference+' - Etude = ' + str(self.etude) + ' - Consultant = ' + str(self.rdm.consultant)
    
    @property
    def realisateur(self):
        return self.rdm.consultant
    
    # Rémunérations brutes : on prend le nombre de JEH et on multiplie par la part étudiante (1-part junior)
    @property
    def remunerationBrute(self):
        return self.rdm.remunerationRaw * (1.0 - self.rdm.percentageJunior)

    @property
    def remunerationBruteParJEH(self):
        return self.rdm.JEHPrice * (1.0 - self.rdm.percentageJunior)

    # Assiette des cotisations = Base URSAFF * nombre de JEH
    @property
    def assietteCotisations(self):
        return getLastBase() * self.rdm.JEHNumber

    @property
    def cotisations_assiette(self):
        return [self.coti_sante, self.coti_accidents, self.coti_retraite_1, self.coti_retraite_2, self.coti_famille, self.coti_autres, self.coti_csg, self.coti_csgcrds, self.coti_exonerations]
    @property
    def cotisations_brutes(self):
        return [self.coti_chomage]

    _VALID_INDEXES = ["all", "assiette", "brutes"]
    def sumColumns(self, attribute, index="all"):
        if not index in self._VALID_INDEXES:
            raise Exception("Valeur de 'index' non valide pour la fonction 'sumColumns'. Indexs valides : " + str(self._VALID_INDEXES))
        sumValues = 0.0
        if(index == "all" or index == "assiette"):
            for coti in self.cotisations_assiette:
                value = getattr(coti, attribute)
                sumValues += value
        if(index == "all" or index == "brutes"):
            for coti in self.cotisations_brutes:
                value = getattr(coti, attribute)
                sumValues += value
        return sumValues

    @property
    def totalCotisations(self):
        sumValues = 0.0
        for coti in self.cotisations_assiette:
            sumValues += (coti.montant_junior + coti.montant_realisateur)
        for coti in self.cotisations_brutes:
            sumValues += (coti.montant_junior + coti.montant_realisateur)
        return sumValues

    @property
    def montant_net(self):
        return self.remunerationBrute - self.sumColumns("montant_realisateur", "all")

    # La fameuse ligne mystère expliquée plus haut xd
    @property
    def evolution_remuneration_supcm(self):
        return (self.taux_sccm_1 - self.taux_sccm_2) * self.assietteCotisations + (self.taux_sccm_3 + self.taux_sccm_4) * self.remunerationBrute

    @property
    def montant_net_imposable(self):
        return self.montant_net + self.coti_csgcrds.montant_realisateur

class BVSerializer(serializers.ModelSerializer):
    rdm = MissionSerializer(read_only=True)
    coti_sante = CotisationSerializer(read_only=False)
    coti_accidents = CotisationSerializer(read_only=False)
    coti_retraite_1 = CotisationSerializer(read_only=False)
    coti_retraite_2 = CotisationSerializer(read_only=False)
    coti_famille = CotisationSerializer(read_only=False)
    coti_chomage = CotisationSerializer(read_only=False)
    coti_autres = CotisationSerializer(read_only=False)
    coti_csg = CotisationSerializer(read_only=False)
    coti_csgcrds = CotisationSerializer(read_only=False)
    coti_exonerations = CotisationSerializer(read_only=False)
    class Meta:
        model = BV
        fields = '__all__'
