from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from flower_app.controllers.permissions import HasGroupPermission, HasAnyGroupPermission
from flower_app.models.Prospection import ContactWay, ContactWaySerializer

class ContactWayListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, HasAnyGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA', 'ROLE_PIOUS'],                                         #
        'POST': ['ROLE_CA', 'ROLE_PIOUS']                                         #
    }
    serializer_class = ContactWaySerializer
    queryset = ContactWay.objects.all()

class ContactWayRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, HasAnyGroupPermission]
    lookup_field = 'id'
    required_groups = {
        'GET': ['ROLE_CA', 'ROLE_PIOUS'],                                         #
        'PUT': ['ROLE_CA', 'ROLE_PIOUS'],                                         #
        'PATCH': ['ROLE_CA', 'ROLE_PIOUS'],                                       #
        'DELETE': ['ROLE_CA','ROLE_PIOUS']                                       #
    }
    serializer_class = ContactWaySerializer
    queryset = ContactWay.objects.all()
