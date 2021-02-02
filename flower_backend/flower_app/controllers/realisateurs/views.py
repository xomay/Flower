from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from flower_app.controllers.permissions import HasGroupPermission
from flower_app.models.People.Realisateur import Realisateur, RealisateurSerializer, RealisateurComment, RealisateurCommentSerializer
from flower_app.models.Competence import Competence, CompetenceSerializer

# Réalisateur

class RealisateurListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA'],                                         #
        'POST': ['ROLE_CA']                                         #
    }
    serializer_class = RealisateurSerializer
    queryset = Realisateur.objects.all()

class RealisateurRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    lookup_field = 'id'
    required_groups = {
        'GET': ['ROLE_CA'],                                         #
        'PUT': ['ROLE_CA'],                                         #
        'PATCH': ['ROLE_CA'],                                       #
        'DELETE': ['ROLE_CA']                                       #
    }
    serializer_class = RealisateurSerializer
    queryset = Realisateur.objects.all()

# Commentaires

class CommentsListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA'],                                         #
        'POST': ['ROLE_CA']                                         #
    }
    serializer_class = RealisateurCommentSerializer
    queryset = RealisateurComment.objects.all()

class CommentsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    lookup_field = 'id'
    required_groups = {
        'GET': ['ROLE_CA'],                                         #
        'PUT': ['ROLE_CA'],                                         #
        'PATCH': ['ROLE_CA'],                                       #
        'DELETE': ['ROLE_CA']                                       #
    }
    serializer_class = RealisateurCommentSerializer
    queryset = RealisateurComment.objects.all()

# Skills

class SkillsRetrieveUpdateDestroyView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA'],                                         #
    }
    serializer_class = CompetenceSerializer
    queryset = Competence.objects.all()