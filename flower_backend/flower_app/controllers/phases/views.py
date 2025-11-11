from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from flower_app.controllers.permissions import HasGroupPermission, HasAnyGroupPermission
from flower_app.models.GroupePhase import Phase, PhaseSerializer, PhaseEtudeSerializer, PhaseEtude, \
    PhaseMissionSerializer, PhaseMission


class PhaseEtudeView(generics.ListCreateAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, HasAnyGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA', 'ROLE_PIOUS'],
        'POST': ['ROLE_CA', 'ROLE_PIOUS'],                                        #from modules/etudes/views/PhaseModifier.vue to add a phase
        'PUT': ['ROLE_CA', 'ROLE_PIOUS'],
        'PATCH': ['ROLE_CA', 'ROLE_PIOUS'],
        'DELETE': ['ROLE_CA', 'ROLE_PIOUS']
    }
    serializer_class = PhaseEtudeSerializer
    queryset = PhaseEtude.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='ROLE_PIOUS').exists() and not user.groups.filter(
                name='ROLE_CA').exists():
            return PhaseEtude.objects.filter(etude__simuetude__isnull=False)
        return PhaseEtude.objects.all()

    def update(self, request):
        serializer = PhaseEtudeSerializer(PhaseEtude.objects.all(), data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def post(self, request):
        serializer = PhaseEtudeSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class PhaseMissionView(generics.ListCreateAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, HasAnyGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA', 'ROLE_PIOUS'],
        'POST': ['ROLE_CA', 'ROLE_PIOUS'],                                        #from modules/etudes/views/PhaseModifier.vue to add a phase
        'PUT': ['ROLE_CA', 'ROLE_PIOUS'],
        'PATCH': ['ROLE_CA', 'ROLE_PIOUS'],
        'DELETE': ['ROLE_CA', 'ROLE_PIOUS']
    }
    serializer_class = PhaseMissionSerializer
    queryset = PhaseMission.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='ROLE_PIOUS').exists() and not user.groups.filter(
                name='ROLE_CA').exists():
            return PhaseMission.objects.filter(mission__project__simuetude__isnull=False)
        return PhaseMission.objects.all()

    def update(self, request):
        serializer = PhaseMissionSerializer(PhaseMission.objects.all(), data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def post(self, request):
        serializer = PhaseMissionSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class PhaseEtudeDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, HasAnyGroupPermission]
    required_groups = {
        'PUT': ['ROLE_CA', 'ROLE_PIOUS'],
        'PATCH': ['ROLE_CA', 'ROLE_PIOUS'],
        'DELETE': ['ROLE_CA', 'ROLE_PIOUS']                                    #from modules/etudes/views/PhaseModifier.vue to delete a phase
    }
    serializer_class = PhaseEtudeSerializer
    queryset = PhaseEtude.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='ROLE_PIOUS').exists() and not user.groups.filter(
                name='ROLE_CA').exists():
            return PhaseEtude.objects.filter(etude__simuetude__isnull=False)
        return PhaseEtude.objects.all()

class PhaseMissionDetailView(generics.DestroyAPIView, generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, HasAnyGroupPermission]
    required_groups = {
        'PUT': ['ROLE_CA', 'ROLE_PIOUS'],
        'DELETE': ['ROLE_CA', 'ROLE_PIOUS']  # from modules/etudes/views/PhaseModifier.vue to delete a phase
    }
    serializer_class = PhaseMissionSerializer
    queryset = PhaseMission.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='ROLE_PIOUS').exists() and not user.groups.filter(
                name='ROLE_CA').exists():
            return PhaseMission.objects.filter(mission__project__simuetude__isnull=False)
        return PhaseMission.objects.all()

    def update(self, request, pk):
        serializer = PhaseMissionSerializer(self.get_object(), data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
