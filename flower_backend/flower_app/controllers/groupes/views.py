from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from flower_app.controllers.permissions import HasGroupPermission
from flower_app.models.GroupePhase import Groupe, GroupeSerializer

class GroupeView(generics.ListCreateAPIView, generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA'],
        'POST': ['ROLE_CA'],                                #from modules/etudes/views/PhaseModifier.vue to add a group
        'PUT': ['ROLE_CA'],                                 #from modules/etudes/views/PhaseModifier.vue to modify the group and his phases
        'PATCH': ['ROLE_CA']
    }
    serializer_class = GroupeSerializer
    queryset = Groupe.objects.all()

    def update(self, request):
        serializer = GroupeSerializer(Groupe.objects.all(), data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class GroupeDetailView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_ADMIN'],
        'PUT': ['ROLE_ADMIN'],
        'DELETE': ['ROLE_CA']                               #from modules/etudes/views/PhaseModifier.vue to delete a group
    }
    serializer_class = GroupeSerializer
    queryset = Groupe.objects.all()
