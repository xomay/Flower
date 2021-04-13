from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response
from http import HTTPStatus

from flower_app.controllers.permissions import HasGroupPermission, is_in_group
from .pil import createSignature
from flower_app.models.People.Membre import Membre

class GenerateSignature(generics.RetrieveAPIView):
    def retrieve(self, request):
        if request.user.is_authenticated and is_in_group(request.user, "ROLE_CA"):
            membre = Membre.objects.get(user=request.user)
            return createSignature(membre)
        return Response("Accès non autorisé.", status=HTTPStatus.UNAUTHORIZED)

