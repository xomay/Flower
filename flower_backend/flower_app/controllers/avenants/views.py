from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from flower_app.controllers.permissions import HasGroupPermission, HasAnyGroupPermission
from flower_app.models.Avenant import AvenantEtude, AvenantMissionSerializer, AvenantMission, AvenantEtudeSerializer, \
    AvenantEtudeDetailSerializer, AvenantMissionDetailSerializer
from flower_app.models.DocEtude import DocEtude, CESerializer, CEDetailSerializer, DocMission, DocMissionSerializer, \
    AvenantEtudeDocSerializer, AvenantDocMissionSerializer


class AvenantEtudeView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, HasAnyGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA', 'ROLE_PIOUS'],
        'POST': ['ROLE_CA', 'ROLE_PIOUS'],
    }
    serializer_class = AvenantEtudeSerializer
    queryset = AvenantEtude.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AvenantEtudeSerializer
        return AvenantEtudeDetailSerializer

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='ROLE_PIOUS').exists() and not user.groups.filter(name='ROLE_CA').exists():
            # Filtrer uniquement les requirements liés à des SimuEtude
            return AvenantEtude.objects.filter(etude__simuetude__isnull=False)
        return AvenantEtude.objects.all()

class AvenantMissionView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, HasAnyGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA', 'ROLE_PIOUS'],
        'POST': ['ROLE_CA', 'ROLE_PIOUS'],
    }
    serializer_class = AvenantMissionSerializer
    queryset = AvenantMission.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AvenantMissionSerializer
        return AvenantMissionDetailSerializer

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='ROLE_PIOUS').exists() and not user.groups.filter(name='ROLE_CA').exists():
            # Filtrer uniquement les requirements liés à des SimuEtude
            return AvenantMission.objects.filter(mission__project__simuetude__isnull=False)
        return AvenantMission.objects.all()


class AvenantEtudeDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, HasAnyGroupPermission]
    required_groups = {
        'PUT': ['ROLE_CA', 'ROLE_PIOUS'],
        'PATCH': ['ROLE_CA', 'ROLE_PIOUS'],
        'DELETE': ['ROLE_CA', 'ROLE_PIOUS']
    }
    queryset = AvenantEtude.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH','DELETE']:
            return AvenantEtudeSerializer
        return AvenantEtudeDetailSerializer

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='ROLE_PIOUS').exists() and not user.groups.filter(name='ROLE_CA').exists():
            # Filtrer uniquement les requirements liés à des SimuEtude
            return AvenantEtude.objects.filter(etude__simuetude__isnull=False)
        return AvenantEtude.objects.all()

    def delete(self, request, *args, **kwargs):
        from flower_app.models.GroupePhase import PhaseEtude
        instance = self.get_object()
        PhaseEtude.objects.filter(avenant_edit=instance).update(state='ACTIVE')

        return self.destroy(request, *args, **kwargs)

class AvenantEtudeDocDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, HasAnyGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA', 'ROLE_PIOUS'],
        'PUT': ['ROLE_CA', 'ROLE_PIOUS'],
        'PATCH': ['ROLE_CA', 'ROLE_PIOUS'],
    }
    queryset = DocEtude.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return AvenantEtudeDocSerializer
        return CEDetailSerializer

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='ROLE_PIOUS').exists() and not user.groups.filter(name='ROLE_CA').exists():
            # Filtrer uniquement les requirements liés à des SimuEtude
            return DocEtude.objects.filter(etude__simuetude__isnull=False)
        return DocEtude.objects.all()


class AvenantMissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, HasAnyGroupPermission]
    required_groups = {
        'PUT': ['ROLE_CA', 'ROLE_PIOUS'],
        'PATCH': ['ROLE_CA', 'ROLE_PIOUS'],
        'DELETE': ['ROLE_CA', 'ROLE_PIOUS']
    }
    queryset = AvenantMission.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH','DELETE']:
            return AvenantMissionSerializer
        return AvenantMissionDetailSerializer

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='ROLE_PIOUS').exists() and not user.groups.filter(name='ROLE_CA').exists():
            # Filtrer uniquement les requirements liés à des SimuEtude
            return AvenantMission.objects.filter(mission__project__simuetude__isnull=False)
        return AvenantMission.objects.all()

    def delete(self, request, *args, **kwargs):
        from flower_app.models.GroupePhase import PhaseMission
        instance = self.get_object()
        PhaseMission.objects.filter(avenant_edit=instance).update(state='ACTIVE')

        return self.destroy(request, *args, **kwargs)

class AvenantDocMissionDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, HasAnyGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA', 'ROLE_PIOUS'],
        'PUT': ['ROLE_CA', 'ROLE_PIOUS'],
        'PATCH': ['ROLE_CA', 'ROLE_PIOUS'],
    }
    queryset = DocMission.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return AvenantDocMissionSerializer
        return DocMissionSerializer

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='ROLE_PIOUS').exists() and not user.groups.filter(name='ROLE_CA').exists():
            # Filtrer uniquement les requirements liés à des SimuEtude
            return DocMission.objects.filter(mission__project__simuetude__isnull=False)
        return DocMission.objects.all()