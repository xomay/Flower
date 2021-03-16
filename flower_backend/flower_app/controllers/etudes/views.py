from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from http import HTTPStatus
from django.http import JsonResponse

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
                    array.append(model_to_dict(mission.project))
                return Response(array, status=HTTPStatus.ACCEPTED)
            else:
                return Response("Il faut être un réalisateur.", status=HTTPStatus.UNAUTHORIZED)
        else:
            return Response(None, status=HTTPStatus.UNAUTHORIZED)

class ReaEtudesDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission, HasReaPermissionToSeeEtude]
    required_groups = {
        'GET': ['ROLE_REA']
    }
    queryset = Etude.objects.all()
    serializer_class = EtudeDetailSerializer

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
