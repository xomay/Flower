from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from flower_app.controllers.permissions import HasGroupPermission
from flower_app.models.GroupePhase import Phase, PhaseSerializer

class PhaseView(generics.ListCreateAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA'],
        'POST': ['ROLE_CA'],                                        #from modules/etudes/views/PhaseModifier.vue to add a phase
        'PUT': ['ROLE_CA'],
        'PATCH': ['ROLE_CA'],
        'DELETE': ['ROLE_CA']
    }
    serializer_class = PhaseSerializer
    queryset = Phase.objects.all()

    def update(self, request):
        serializer = PhaseSerializer(Phase.objects.all(), data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class PhaseDetailView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'DELETE': ['ROLE_CA']                                       #from modules/etudes/views/PhaseModifier.vue to delete a phase
    }
    serializer_class = PhaseSerializer
    queryset = Phase.objects.all()
