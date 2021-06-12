from ...models.Etude import Etude
from ...models.GroupePhase import GroupesSetSerializer, GroupesSet, Phase, US
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from rest_framework import generics
from http import HTTPStatus
from ..permissions import HasGroupPermission
from ...models.Avenant import AvenantSerializer, Avenant

class AvenantListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA'],
        'POST': ['ROLE_CA']
    }
    serializer_class = AvenantSerializer
    queryset = Avenant.objects.all()

    def post(self, request, *args, **kwargs):
        etude = Etude.objects.get(pk=request._data['project'])
        originalGS = etude.currentGroupes.groupe_set
        instance = self.create(request, *args, **kwargs)
        # Cloner tous les groupes,phases,us
        for groupe in originalGS.all():
            allPhasesIds = list()
            for phase in groupe.phase_set.all():
                allUsIds = list()
                for us in phase.us_set.all():
                    us.pk = None
                    us.save()
                    allUsIds.append(us.pk)
                phase.pk = None
                phase.save()
                for newUsID in allUsIds:
                    us = US.objects.get(pk=newUsID)
                    us.phase = phase
                    us.save()
                allPhasesIds.append(phase.pk)
            groupe.pk = None    #Pour cloner un objet, on reset sa PK et on le #save.
            groupe.owner = GroupesSet.objects.get(id=instance.data['groupes']['id'])
            groupe.save()
            for newPhaseID in allPhasesIds:
                phase = Phase.objects.get(pk=newPhaseID)
                phase.groupe = groupe
                phase.save()
            
            gs = GroupesSet.objects.get(id=instance.data['groupes']['id'])
            gss = GroupesSetSerializer(gs)
        return JsonResponse(gss.data, status=HTTPStatus.OK)

class AvenantRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA'],
        'PUT': ['ROLE_CA'],
        'PATCH': ['ROLE_CA'],
        'DELETE': ['ROLE_CA']
    }
    serializer_class = AvenantSerializer
    queryset = Avenant.objects.all()
