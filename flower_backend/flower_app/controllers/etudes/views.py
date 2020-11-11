from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from flower_app.controllers.permissions import HasGroupPermission
from flower_app.models.CE import CE, CESerializer, CEDetailSerializer
from flower_app.models.Etude import Etude, EtudeSerializer, EtudeDetailSerializer
# from flower_app.models.Groupe import Groupe, GroupeSerializer
from flower_app.models.GroupePhase import Groupe, Phase, GroupeSerializer, PhaseSerializer
from flower_app.models.Mission import Mission, MissionSerializer, MissionDetailSerializer

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
        'GET': ['ROLE_CA'],                                     #from modules/etudes/views/project/EtudeModifier.vue or modules/etudes/views/project/EtudeDetail.vue
                                                                #   or modules/etudes/views/PhaseModifier.vue or modules/etudes/views/projectConvention/EtudeConvention.vue
                                                                #   or modules/etudes/views/MissionCreer.vue beforeCreate or modules/etudes/views/PVRCreator.vue or
                                                                #   modules/etudes/views/PVREditor.vue
        'PUT': ['ROLE_CA'],                                     #from modules/etudes/views/project/EtudeModifier.vue to save
        'PATCH': ['ROLE_CA']
    }
    queryset = Etude.objects.all()

    def get_serializer_class(self):        
        if self.request.method in ['PUT', 'PATCH']:
            return EtudeSerializer
        return EtudeDetailSerializer

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
