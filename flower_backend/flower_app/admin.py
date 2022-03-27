from django.contrib import admin
from .models.CE import CE
from .models.People.Employe import Employe
from .models.Etude import Etude
from .models.Facture import Facture
from .models.FactureDetail import FactureDetail
# from .models.Groupe import Groupe
from .models.People.Membre import Membre
from .models.People.Realisateur import Realisateur, RealisateurComment
from .models.Mission import Mission
from .models.PVR import PVR
from .models.GroupePhase import GroupesSet, Groupe, Phase, US
from .models.People.Prospect import Prospect
from .models.Prospection import Action, TypeAction, ContactWay
from .models.Competence import Competence
from .models.ParamsJE import ParamsJE
from .models.NdF import NdF
from .models.NdFDetail import NdFDetail
from .models.Poste import Poste
from .models.UploadedFile import UploadedFile
from .models.BaseUrsaff import BaseUrsaff
from .models.BV import BV, Cotisation
from .models.Avenant import Avenant
from .models.BA import BA

# Register your models here.
admin.site.register(CE)
admin.site.register(Employe)
admin.site.register(Etude)
admin.site.register(Facture)
admin.site.register(FactureDetail)
admin.site.register(Groupe)
admin.site.register(Membre)
admin.site.register(Mission)
admin.site.register(PVR)
admin.site.register(Phase)
admin.site.register(Prospect)
admin.site.register(ContactWay)
admin.site.register(TypeAction)
admin.site.register(Action)
admin.site.register(Realisateur)
admin.site.register(RealisateurComment)
admin.site.register(BA)
admin.site.register(Competence)
admin.site.register(ParamsJE)
admin.site.register(NdF)
admin.site.register(NdFDetail)
admin.site.register(US)
admin.site.register(Poste)
admin.site.register(UploadedFile)
admin.site.register(BaseUrsaff)
admin.site.register(BV)
admin.site.register(Cotisation)
admin.site.register(GroupesSet)
admin.site.register(Avenant)
