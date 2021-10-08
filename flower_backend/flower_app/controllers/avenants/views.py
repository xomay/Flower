from ...models.Etude import Etude
from ...models.GroupePhase import GroupesSetSerializer, GroupesSet, Phase, US
from ...models.People.Membre import Membre
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
        if not etude.canBeEdited:
            JsonResponse({'message': "L'étude n'est pas modifiable."}, status=HTTPStatus.FORBIDDEN)
        originalGS = etude.currentGroupes.groupe_set

        id_instance = self.create(request, *args, **kwargs).data['id']
        instance = Avenant.objects.get(id=id_instance)
        allPhasesIDs = [] # ce tableau est utilisé pour savoir tous les ID de phases qui existent pour les rdm en dessous
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
                allPhasesIDs.append(phase.id)
                for newUsID in allUsIds:
                    us = US.objects.get(pk=newUsID)
                    us.phase = phase
                    us.save()
                allPhasesIds.append(phase.pk)
            groupe.pk = None    #Pour cloner un objet, on reset sa PK et on le #save.
            groupe.owner = GroupesSet.objects.get(id=instance.groupes.id)
            groupe.save()
            for newPhaseID in allPhasesIds:
                phase = Phase.objects.get(pk=newPhaseID)
                phase.groupe = groupe
                phase.save()
            
        gs = GroupesSet.objects.get(id=instance.groupes.id)
        gss = GroupesSetSerializer(gs)

        if not (Membre.objects.filter(user=request.user).first() is None):
            instance.author = request.user.member
            instance.save()

        # Maintenant que les phases ont été migrées, on modifie les RM de l'étude.
        #for rdm in etude.mission_set.all():
        #    amountPhases = 0
        #    for rdm_phase in rdm.phases.all():
        #        if rdm_phase.id in allPhasesIDs:
        #            amountPhases += 1
        #        else:
        #            # la phase a été supprimée
        #            rdm.phases.remove(rdm_phase)
        #            pass
        #    # Si jamais on a 0 phases dans la RDM, on devrait la supprimer.
        #    #Je vais éviter de le faire ici, c'est un choix.

        return JsonResponse({
            'groupes': gss.data,
            'id': instance.id
        }, status=HTTPStatus.OK)

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
