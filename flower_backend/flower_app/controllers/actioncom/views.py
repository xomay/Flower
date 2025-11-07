from http import HTTPStatus

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from flower_app.controllers.permissions import HasGroupPermission, HasAnyGroupPermission
from flower_app.models.Prospection import Action, ActionSerializer, TypeAction, TypeActionSerializer, SimuAction


class ActionsCommercialesListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, HasAnyGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA', 'ROLE_PIOUS'],                                         #from modules/TODO
        'POST': ['ROLE_CA', 'ROLE_PIOUS']                                     #from modules/TODO
    }
    serializer_class = ActionSerializer
    queryset = Action.objects.all()

    def get_queryset(self):
        if self.request.user.groups.filter(name='ROLE_PIOUS').exists() and not self.request.user.groups.filter(
                name='ROLE_CA').exists():
            return SimuAction.objects.all()
        return Action.objects.all()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not self.request.user.groups.filter(name__in=['ROLE_PIOUS','ROLE_CA']).exists():
            return Response({"detail": "Vous n'avez pas la permission d'accéder à cette ressource."}, status=HTTPStatus.FORBIDDEN)

        data = serializer.validated_data.copy()

        # On retire les M2M avant création
        participants = data.pop('participants', [])

        if self.request.user.groups.filter(name='ROLE_PIOUS').exists() and not self.request.user.groups.filter(
            name='ROLE_CA').exists():
            new_action = SimuAction.objects.create(**data)
        else:
            new_action = Action.objects.create(**data)

        # On ré-associe les relations M2M après la création
        if participants:
            new_action.participants.set(participants)

        serializer = ActionSerializer(new_action)
        return Response(serializer.data, status=HTTPStatus.CREATED)

class ActionsCommercialesDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, HasAnyGroupPermission]
    lookup_field = 'id'
    required_groups = {
        'GET': ['ROLE_CA', 'ROLE_PIOUS'],                                     #from modules/TODO
        'PUT': ['ROLE_CA', 'ROLE_PIOUS'],                                     #from modules/TODO
        'PATCH': ['ROLE_CA', 'ROLE_PIOUS'],
        'DELETE': ['ROLE_CA', 'ROLE_PIOUS']                                   #from modules/TODO
    }
    serializer_class = ActionSerializer
    queryset = Action.objects.all()

    def get_queryset(self):
        if self.request.user.groups.filter(name='ROLE_PIOUS').exists() and not self.request.user.groups.filter(
                name='ROLE_CA').exists():
            return SimuAction.objects.all()
        return Action.objects.all()

class ActionsTypesView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, HasAnyGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA', 'ROLE_PIOUS'],                                     #from modules/TODO
        'POST': ['ROLE_CA', 'ROLE_PIOUS']                                     #from modules/TODO
    }
    serializer_class = TypeActionSerializer
    queryset = TypeAction.objects.all()
