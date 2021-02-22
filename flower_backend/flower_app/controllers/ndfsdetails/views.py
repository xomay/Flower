from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from flower_app.controllers.permissions import HasGroupPermission
from flower_app.models.NdFDetail import NdFDetail, NdFDetailSerializer

class NdFDetailView(generics.ListCreateAPIView, generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA', 'ROLE_TRESO'],
        'POST': ['ROLE_CA', 'ROLE_TRESO'],                                #from modules/etudes/views/PhaseModifier.vue to add a group
        'PUT': ['ROLE_CA', 'ROLE_TRESO'],                                 #from modules/etudes/views/PhaseModifier.vue to modify the group and his phases
        'PATCH': ['ROLE_CA', 'ROLE_TRESO']
    }
    serializer_class = NdFDetailSerializer
    queryset = NdFDetail.objects.all()

    def update(self, request):
        serializer = NdFDetailSerializer(NdFDetail.objects.all(), data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class NdFDetailDetailView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'DELETE': ['ROLE_CA', 'ROLE_TRESO']                               #from modules/etudes/views/PhaseModifier.vue to delete a group
    }
    serializer_class = NdFDetailSerializer
    queryset = NdFDetail.objects.all()
