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
from .models.GroupePhase import Groupe, Phase
from .models.People.Prospect import Prospect
from .models.Prospection import Action, TypeAction, ContactWay

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
