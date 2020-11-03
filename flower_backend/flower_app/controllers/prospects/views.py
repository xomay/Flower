from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from flower_app.controllers.permissions import HasGroupPermission
from flower_app.models.People.Prospect import Prospect, ProspectSerializer
from flower_app.models.People.Employe import Employe, EmployeSerializer

class ProspectListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA'],
        'POST': ['ROLE_CA']
    }
    serializer_class = ProspectSerializer
    queryset = Prospect.objects.all()

class ProspectRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA'],
        'PUT': ['ROLE_CA'],
        'PATCH': ['ROLE_CA'],
        'DELETE': ['ROLE_CA']
    }
    serializer_class = ProspectSerializer
    queryset = Prospect.objects.all()

class EmployeListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA'],
        'POST': ['ROLE_CA']
    }
    serializer_class = EmployeSerializer
    def get_queryset(self):
        prospectId = self.kwargs.get('id')
        # Searching employees from a prospect
        employes = Prospect.objects.get(id=prospectId).employe_set
        return employes
    
    def create(self, request, id):
        request.data['prospect'] = id
        return super().create(request)

class EmployeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA'],
        'PUT': ['ROLE_CA'],
        'PATCH': ['ROLE_CA'],
        'DELETE': ['ROLE_CA']
    }
    serializer_class = EmployeSerializer
    queryset = Employe.objects.all()
    lookup_field = 'id'
