from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from http import HTTPStatus

from flower_app.controllers.permissions import HasGroupPermission, HasReaPermissionToSeeEtude, is_in_group, \
    HasAnyGroupPermission
from flower_app.models.GroupePhase import US, USSerializer
from flower_app.models.People.Realisateur import Realisateur

class USView(generics.ListCreateAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, HasAnyGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA', 'ROLE_PIOUS'],
        'POST': ['ROLE_CA', 'ROLE_PIOUS'],
        'PUT': ['ROLE_CA', 'ROLE_PIOUS'],
        'PATCH': ['ROLE_CA', 'ROLE_PIOUS'],
        'DELETE': ['ROLE_CA', 'ROLE_PIOUS']
    }
    serializer_class = USSerializer
    queryset = US.objects.all()

    def update(self, request):
        serializer = USSerializer(US.objects.all(), data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class USDetailView(generics.DestroyAPIView, generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, HasAnyGroupPermission]
    required_groups = {
        'PUT': ['ROLE_CA', 'ROLE_PIOUS'],
        'DELETE': ['ROLE_CA', 'ROLE_PIOUS']
    }
    serializer_class = USSerializer
    queryset = US.objects.all()

class ReaUpdateUSView(generics.UpdateAPIView):
    def update(self, request, uss_id, new_state):
        if(not [item for item in US.US_STATES if item[0] == new_state]):
            return Response("Cette valeur de new_state ("+str(new_state)+") n'est pas autorisée.", status=HTTPStatus.UNAUTHORIZED)
        us_instance = US.objects.get(pk=uss_id)
        try:
            rea = Realisateur.objects.get(user=request.user)
            if( not is_in_group(request.user, "ROLE_REA")):
                raise Exception() # Go to the except clause
            try:
                rea.mission_set.get(project=us_instance.phase.groupe.project)
                if(us_instance.state == US.US_STATES[0][0] or us_instance.state == US.US_STATES[-1][0]):
                    return Response("Il est interdit de choisir la première ou dernière étape.", status=HTTPStatus.UNAUTHORIZED)
                us_instance.state = new_state
                us_instance.save()
                return Response(new_state)
            except:
                return Response("Accès non autorisé", status=HTTPStatus.UNAUTHORIZED)
        except:
            return Response("Vous n'êtes pas authentifié comme un réalisateur.", status=HTTPStatus.UNAUTHORIZED)