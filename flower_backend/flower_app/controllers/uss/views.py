from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from flower_app.controllers.permissions import HasGroupPermission
from flower_app.models.GroupePhase import US, USSerializer

class USView(generics.ListCreateAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA'],
        'POST': ['ROLE_CA'],
        'PUT': ['ROLE_CA'],
        'PATCH': ['ROLE_CA'],
        'DELETE': ['ROLE_CA']
    }
    serializer_class = USSerializer
    queryset = US.objects.all()

    def update(self, request):
        serializer = USSerializer(US.objects.all(), data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class USDetailView(generics.DestroyAPIView, generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'PUT': ['ROLE_CA'],
        'DELETE': ['ROLE_CA']
    }
    serializer_class = USSerializer
    queryset = US.objects.all()
