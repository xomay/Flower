from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.shortcuts import get_object_or_404

from flower_app.controllers.permissions import HasGroupPermission
from flower_app.models.ParamsJE import ParamsJE, ParamsJESerializer

class GetParametersJE(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA'],
        'POST': ['ROLE_ADMIN'],
        'PUT': ['ROLE_ADMIN']
    }
    serializer_class = ParamsJESerializer
    queryset = ParamsJE.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=1)
        return obj
