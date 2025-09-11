from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from flower_app.controllers.permissions import HasGroupPermission
from flower_app.models.GroupePhase import Phase, PhaseSerializer, PhaseEtudeSerializer, PhaseEtude, \
    PhaseMissionSerializer, PhaseMission


class PhaseEtudeView(generics.ListCreateAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA'],
        'POST': ['ROLE_CA'],                                        #from modules/etudes/views/PhaseModifier.vue to add a phase
        'PUT': ['ROLE_CA'],
        'PATCH': ['ROLE_CA'],
        'DELETE': ['ROLE_CA']
    }
    serializer_class = PhaseEtudeSerializer
    queryset = PhaseEtude.objects.all()

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
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA'],
        'POST': ['ROLE_CA'],                                        #from modules/etudes/views/PhaseModifier.vue to add a phase
        'PUT': ['ROLE_CA'],
        'PATCH': ['ROLE_CA'],
        'DELETE': ['ROLE_CA']
    }
    serializer_class = PhaseMissionSerializer
    queryset = PhaseMission.objects.all()

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
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'PUT': ['ROLE_CA'],
        'PATCH': ['ROLE_CA'],
        'DELETE': ['ROLE_CA']                                    #from modules/etudes/views/PhaseModifier.vue to delete a phase
    }
    serializer_class = PhaseEtudeSerializer
    queryset = PhaseEtude.objects.all()

class PhaseMissionDetailView(generics.DestroyAPIView, generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'PUT': ['ROLE_CA'],
        'DELETE': ['ROLE_CA']  # from modules/etudes/views/PhaseModifier.vue to delete a phase
    }
    serializer_class = PhaseMissionSerializer
    queryset = PhaseMission.objects.all()

    def update(self, request, pk):
        serializer = PhaseMissionSerializer(self.get_object(), data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
