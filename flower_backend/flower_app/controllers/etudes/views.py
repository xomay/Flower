from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from http import HTTPStatus
from django.http import JsonResponse
from datetime import datetime

from flower_app.controllers.permissions import HasGroupPermission, HasReaPermissionToSeeEtude
from flower_app.models.CE import CE, CESerializer, CEDetailSerializer
from flower_app.models.Etude import Etude, EtudeSerializer, EtudeDetailSerializer
from flower_app.models.UploadedFile import UploadedFile, UploadedFileSerializer
from flower_app.models.GroupePhase import Groupe, Phase, GroupeSerializer, PhaseSerializer
from flower_app.models.Mission import Mission, MissionSerializer, MissionDetailSerializer
from flower_app.models.People.Realisateur import Realisateur

from flower_app.controllers.permissions import is_in_group
from django.forms.models import model_to_dict

class EtudeListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA'],                                     #from modules/etudes/views/EtudeVoir.vue
        'POST': ['ROLE_CA']                                     #from modules/etudes/views/project/EtudeCreer.vue
    }
    serializer_class = EtudeSerializer
    queryset = Etude.objects.all()

class EtudeRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA'],
        'PUT': ['ROLE_CA'],
        'PATCH': ['ROLE_CA']
    }
    queryset = Etude.objects.all()

    def get_serializer_class(self):        
        if self.request.method in ['PUT', 'PATCH']:
            return EtudeSerializer
        return EtudeDetailSerializer

class EtudeEditFiles(APIView):
    def put(self, request, id):
        if not request.user.is_authenticated:
            return Response("You are not authenticated.", status=HTTPStatus.UNAUTHORIZED)
        etude = Etude.objects.get(pk=id)
        mode = request.data['mode']
        file = UploadedFile.objects.get(pk=request.data['file_id'])
        if(mode == "add"):
            etude.linkedFiles.add(file)
            etude.save()
            dtt = UploadedFileSerializer(file, read_only=True)
            return JsonResponse(dtt.data, status=HTTPStatus.OK)
        elif(mode == "remove"):
            etude.linkedFiles.remove(file)
            etude.save()
            if(request.data['delete_file'] == True):
                file.delete()
            return Response(None, status=HTTPStatus.OK)
        return Response("Il faut préciser le mode", status=HTTPStatus.NOT_ACCEPTABLE)

class ReaEtudesView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            if is_in_group(request.user, 'ROLE_REA'):
                array = []
                realisateur = Realisateur.objects.get(user=request.user)
                for mission in realisateur.mission_set.all():
                    array.append({
                        'id': mission.project.id,
                        'name': mission.project.name,
                        'state': mission.project.state,
                        'mandat': mission.project.mandat,
                        'number': mission.project.number
                    })
                return Response(array, status=HTTPStatus.ACCEPTED)
            else:
                return Response("Il faut être un réalisateur.", status=HTTPStatus.UNAUTHORIZED)
        else:
            return Response(None, status=HTTPStatus.UNAUTHORIZED)

class ReaEtudesDetailView(generics.RetrieveAPIView):
    #   Grosse méthode je sais x)
    #   Le but, c'est de : 1) vérifier que le réa à le droit d'être là (et que c'est bien un réa xd)
    #   Deux, et c'est ce qui rend la chose complexe, on veut absolument qu'il ait plus d'informations que nécessaire.
    # Pour ça, on récupère toutes les phases concernées par sa mission, PUIS on récupère les groupes en fonction des phases concernées,
    # et on réassemble le tout pour lui renvoyer.
    def get(self, request, etude_id):
        # On vérifie que la personne connectée ait le droit d'être ici.
        etude_instance = Etude.objects.get(pk=etude_id)
        try:
            realisateur = Realisateur.objects.get(user=request.user) # récupérer le réa associé à la requete
            rdm = realisateur.mission_set.get(project=etude_instance) # vérifier qu'il existe au moins une mission qui lie ce réa à cette étude
        except:
            return Response(None, status=HTTPStatus.UNAUTHORIZED)
        if( not is_in_group(request.user, 'ROLE_REA')):
            return Response("Il faut la permission de réalisateur.", status=HTTPStatus.UNAUTHORIZED)
        # On prépare les données générales de l'étude, avec le strict nécessaire.
        data = {
            'id': etude_instance.id,
            'name': etude_instance.name,
            'state': etude_instance.state,
            'mandat': etude_instance.mandat,
            'number': etude_instance.number,
            'description': etude_instance.description,
            'projectManager': {
                'firstname': etude_instance.projectManager.firstname,
                'lastname': etude_instance.projectManager.lastname,
            },
            'groupes': []
        }
        groupes = []
        phases = list()
        # On récupère et serialize toutes les phases auxquelles le réa à accès, et pas plus.
        for phase in rdm.phases.all():
            uss = []
            for p_us in phase.us_set.all():
                uss.append({
                    'id': p_us.id,
                    'index': p_us.index,
                    'state': p_us.state,
                })
            phases.append({
                'id': phase.id,
                'title': phase.title,
                'index': phase.index,
                'description': phase.description,
                'beginDate': phase.beginDate,
                'period': phase.period,
                'groupe': phase.groupe.id,
                'uss': uss
            })

        # Enfin on prend tous les groupes de l'étude, et si des phases plus haut a été sérialisée, on
        # le sérialize lui aussi avant de rajouter la ou les étapes qui le concernent.
        groupes_ids = list() #  ceux déjà faits
        for groupe in etude_instance.groupe_set.all():
            for phase in phases:
                if(phase['groupe'] == groupe.id):
                    # Groupe pas encore rencontré, on le sérialize
                    if not groupe.id in groupes_ids:
                        groupes_ids.append(groupe.id)
                        groupes.append({
                            'id': groupe.id,
                            'title': groupe.title,
                            'index': groupe.index,
                            'description': groupe.description,
                            'phases': []
                        })
                    # Récupérer le groupe pour y rajouter cette phase
                    for g_dict in groupes:
                        if g_dict['id'] == groupe.id:
                            g_dict['phases'].append(phase)
                            break
        # Rajouter les groupes sérialisés aux données à envoyer, puis renvoyer tout ça.
        data['groupes'] = groupes
        return Response(data, status=HTTPStatus.OK)

class CEView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA'],
        'PUT': ['ROLE_CA'],
        'PATCH': ['ROLE_CA']
    }
    serializer_class = CESerializer
    def retrieve(self, request, pk):
        return Response(CEDetailSerializer(Etude.objects.get(id=pk).ce).data)

    def update(self, request, pk):
        serializer = CESerializer(data=request.data)
        if (serializer.is_valid(raise_exception=True)):
            CE.objects.filter(id=request.data['id']).update(**serializer.data)
            return Response(serializer.data)
        return Response()

class MissionsView(generics.ListCreateAPIView, generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA'],
        'POST': ['ROLE_CA'],                                        # from modules/etudes/views/MissionCreer.vue
        'PUT': ['ROLE_CA'],                                         # from modules/etudes/views/MissionCreer.vue
        'PATCH': ['ROLE_CA']
    }
    serializer_class = MissionSerializer
    lookup_url_kwarg = "project_id"

    def get_serializer_class(self):        
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return MissionSerializer
        return MissionDetailSerializer

    def get_queryset(self):
        return Etude.objects.get(id=self.kwargs.get('pk')).mission_set

    def update(self, request, pk):
        serializer = MissionSerializer(Mission.objects.all(), data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class MissionsDetailView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'DELETE': ['ROLE_CA']                                   #from from modules/etudes/components/forms/MissionForm.vue in modules/etudes/views/MissionCreer.vue
    }
    serializer_class = MissionSerializer
    queryset = Mission.objects.all()
