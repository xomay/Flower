from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from flower_app.controllers.permissions import HasGroupPermission
from flower_app.models.Prospection import ContactWay, ContactWaySerializer

class ContactWayListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA'],                                         #
        'POST': ['ROLE_CA']                                         #
    }
    serializer_class = ContactWaySerializer
    queryset = ContactWay.objects.all()

class ContactWayRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    lookup_field = 'id'
    required_groups = {
        'GET': ['ROLE_CA'],                                         #
        'PUT': ['ROLE_CA'],                                         #
        'PATCH': ['ROLE_CA'],                                       #
        'DELETE': ['ROLE_CA']                                       #
    }
    serializer_class = ContactWaySerializer
    queryset = ContactWay.objects.all()
