from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from flower_app.controllers.permissions import HasGroupPermission
from flower_app.models.Avenant import AvenantEtude, AvenantMissionSerializer, AvenantMission, AvenantEtudeSerializer, \
    AvenantEtudeDetailSerializer, AvenantMissionDetailSerializer
from flower_app.models.DocEtude import DocEtude, CESerializer, CEDetailSerializer, DocMission, DocMissionSerializer, \
    AvenantEtudeDocSerializer, AvenantDocMissionSerializer


class AvenantEtudeView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA'],
        'POST': ['ROLE_CA'],
    }
    serializer_class = AvenantEtudeSerializer
    queryset = AvenantEtude.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AvenantEtudeSerializer
        return AvenantEtudeDetailSerializer

class AvenantMissionView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA'],
        'POST': ['ROLE_CA'],
    }
    serializer_class = AvenantMissionSerializer
    queryset = AvenantMission.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AvenantMissionSerializer
        return AvenantMissionDetailSerializer


class AvenantEtudeDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'PUT': ['ROLE_CA'],
        'PATCH': ['ROLE_CA'],
        'DELETE': ['ROLE_CA']
    }
    queryset = AvenantEtude.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH','DELETE']:
            return AvenantEtudeSerializer
        return AvenantEtudeDetailSerializer

    def delete(self, request, *args, **kwargs):
        from flower_app.models.GroupePhase import PhaseEtude
        instance = self.get_object()
        PhaseEtude.objects.filter(avenant_edit=instance).update(state='ACTIVE')

        return self.destroy(request, *args, **kwargs)

class AvenantEtudeDocDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA'],
        'PUT': ['ROLE_CA'],
        'PATCH': ['ROLE_CA'],
    }
    queryset = DocEtude.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return AvenantEtudeDocSerializer
        return CEDetailSerializer


class AvenantMissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'PUT': ['ROLE_CA'],
        'PATCH': ['ROLE_CA'],
        'DELETE': ['ROLE_CA']
    }
    queryset = AvenantMission.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH','DELETE']:
            return AvenantMissionSerializer
        return AvenantMissionDetailSerializer

    def delete(self, request, *args, **kwargs):
        from flower_app.models.GroupePhase import PhaseMission
        instance = self.get_object()
        PhaseMission.objects.filter(avenant_edit=instance).update(state='ACTIVE')

        return self.destroy(request, *args, **kwargs)

class AvenantDocMissionDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA'],
        'PUT': ['ROLE_CA'],
        'PATCH': ['ROLE_CA'],
    }
    queryset = DocMission.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return AvenantDocMissionSerializer
        return DocMissionSerializer