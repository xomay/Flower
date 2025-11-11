from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from flower_app.controllers.permissions import HasGroupPermission, HasAnyGroupPermission
from flower_app.models.PVR import PVR, PVRSerializer

class PVRListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, HasAnyGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA', 'ROLE_PIOUS'],
        'POST': ['ROLE_CA', 'ROLE_PIOUS']                                     #from modules/etudes/views/PVRCreator.view
    }
    serializer_class = PVRSerializer
    queryset = PVR.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='ROLE_PIOUS').exists() and not user.groups.filter(name='ROLE_CA').exists():
            # Filtrer uniquement les requirements liés à des SimuEtude
            return PVR.objects.filter(project__simuetude__isnull=False)
        return PVR.objects.all()

class PVRRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, HasAnyGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA', 'ROLE_PIOUS'],                                     #from modules/etudes/views/PVREditor.view
        'PUT': ['ROLE_CA', 'ROLE_PIOUS'],                                     #from modules/etudes/views/PVREditor.view
        'PATCH': ['ROLE_CA', 'ROLE_PIOUS'],
        'DELETE': ['ROLE_CA', 'ROLE_PIOUS']                                   #from modules/etudes/components/Generation.vue in modules/etudes/views/EtudeDetail.vue
    }
    serializer_class = PVRSerializer
    queryset = PVR.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='ROLE_PIOUS').exists() and not user.groups.filter(name='ROLE_CA').exists():
            # Filtrer uniquement les requirements liés à des SimuEtude
            return PVR.objects.filter(project__simuetude__isnull=False)
        return PVR.objects.all()
