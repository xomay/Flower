from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from flower_app.controllers.permissions import HasGroupPermission
from flower_app.models.PVR import PVR, PVRSerializer

class PVRListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA', 'ROLE_TRESO'],
        'POST': ['ROLE_CA', 'ROLE_TRESO']                                     #from modules/etudes/views/PVRCreator.view
    }
    serializer_class = PVRSerializer
    queryset = PVR.objects.all()

class PVRRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA', 'ROLE_TRESO'],                                     #from modules/etudes/views/PVREditor.view
        'PUT': ['ROLE_CA', 'ROLE_TRESO'],                                     #from modules/etudes/views/PVREditor.view
        'PATCH': ['ROLE_CA', 'ROLE_TRESO'],
        'DELETE': ['ROLE_CA', 'ROLE_TRESO']                                   #from modules/etudes/components/Generation.vue in modules/etudes/views/EtudeDetail.vue
    }
    serializer_class = PVRSerializer
    queryset = PVR.objects.all()
