from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response
from http import HTTPStatus

from flower_app.controllers.permissions import HasGroupPermission, is_in_group
from .gantt import computeGanttFromEtude
from flower_app.models.Etude import Etude
from flower_app.models.People.Realisateur import Realisateur

def send_gantt(etude, requestSelf):
    return computeGanttFromEtude(etude, image_format=requestSelf.query_params.get('type', 'jpg'))

class GanttView(generics.RetrieveAPIView):
    # J'ai fais ce gros bazar, car le comportement en fonction de si c'est un réa ou pas.
    def retrieve(self, request, etude_id):
        etude = Etude.objects.get(pk=etude_id)
        # Cas réalisateur : si il fait partie de l'étude, il peut accéder. Sinon, non.
        if(is_in_group(request.user, "ROLE_REA")):
            try:
                Realisateur.objects.get(user=request.user).mission_set.get(project=etude)
                return send_gantt(etude, self.request)
            except:
                return Response("Accès non autorisé", status=HTTPStatus.UNAUTHORIZED)
        # C'est un memebre du CA ? Ben c'est bon on envoie
        if(is_in_group(request.user, "ROLE_CA")):
            return send_gantt(etude, self.request)
        # Des fois que ce soit un parfait inconnu, on refuse.
        return Response("Accès non autorisé.", status=HTTPStatus.UNAUTHORIZED)

