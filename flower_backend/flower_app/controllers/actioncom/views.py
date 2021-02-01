from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from flower_app.controllers.permissions import HasGroupPermission
from flower_app.models.Prospection import Action, ActionSerializer, TypeAction, TypeActionSerializer

class ActionsCommercialesListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA'],
        'POST': ['ROLE_CA']                                     #from modules/TODO
    }
    serializer_class = ActionSerializer
    queryset = Action.objects.all()

class ActionsCommercialesDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    lookup_field = 'id'
    required_groups = {
        'GET': ['ROLE_CA'],                                     #from modules/TODO
        'PUT': ['ROLE_CA'],                                     #from modules/TODO
        'PATCH': ['ROLE_CA'],
        'DELETE': ['ROLE_CA']                                   #from modules/TODO
    }
    serializer_class = ActionSerializer
    queryset = Action.objects.all()

class ActionsTypesView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA'],
        'POST': ['ROLE_CA']                                     #from modules/TODO
    }
    serializer_class = TypeActionSerializer
    queryset = TypeAction.objects.all()
