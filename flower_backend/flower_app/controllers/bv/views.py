from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from flower_app.controllers.permissions import HasGroupPermission
from flower_app.models.BV import BV, BVSerializer

class BVView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA', 'ROLE_TRESO'],
        'POST': ['ROLE_CA', 'ROLE_TRESO']
    }
    serializer_class = BVSerializer
    queryset = BV.objects.all()

class BVDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA', 'ROLE_TRESO'],
        'PUT': ['ROLE_CA', 'ROLE_TRESO'],
        'PATCH': ['ROLE_CA', 'ROLE_TRESO'],
        'DELETE': ['ROLE_CA', 'ROLE_TRESO']
    }
    serializer_class = BVSerializer
    queryset = BV.objects.all()
