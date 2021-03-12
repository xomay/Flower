from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from http import HTTPStatus
import random
import string
from django.contrib.auth.models import User, Group

from flower_app.controllers.permissions import HasGroupPermission
from flower_app.models.People.Realisateur import Realisateur, RealisateurSerializer, RealisateurComment, RealisateurCommentSerializer
from flower_app.models.Competence import Competence, CompetenceSerializer

from flower_app.email.mail_reas_accounts import send_mail_rea_account_creation, send_mail_rea_account_deletion

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
        'GET': ['ROLE_CA'],
        'PUT': ['ROLE_CA'],
        'PATCH': ['ROLE_CA'],
        'DELETE': ['ROLE_CA']
    }
    serializer_class = RealisateurSerializer
    queryset = Realisateur.objects.all()

class OpenAccountView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'PUT': ['ROLE_ADMIN'],
    }
    serializer_class = RealisateurSerializer
    queryset = Realisateur.objects.all()
    def update(self, request, pk):
        realisateur = Realisateur.objects.get(id=pk)
        new_username = "{firstname}.{lastname}".format(firstname=realisateur.firstname, lastname=realisateur.lastname).replace(" ", "").lower()
        new_password = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(16))
        newAccount = User.objects.create_user(
            username=new_username,
            email=realisateur.email_insa,
            password=new_password
        )
        newAccount.save()
        realisateur.user = newAccount
        realisateur.save()
        groupRea = Group.objects.get(name='ROLE_REA') 
        groupRea.user_set.add(newAccount)
        try:
            send_mail_rea_account_creation(realisateur, new_username, new_password)
        except:
            print("Impossible d'envoyer l'email !")
        return Response(data={"username": newAccount.username}, status=HTTPStatus.CREATED)

class DeleteAccountView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'PUT': ['ROLE_ADMIN'],
    }
    serializer_class = RealisateurSerializer
    queryset = Realisateur.objects.all()
    def update(self, request, pk):
        realisateur = Realisateur.objects.get(id=pk)
        account = realisateur.user
        Group.objects.get(name='ROLE_REA').user_set.remove(account)
        realisateur.user = None
        realisateur.save()
        account.delete()
        try:
            send_mail_rea_account_deletion(realisateur)
        except:
            print("Impossible d'envoyer l'email !")
        return Response(None, status=HTTPStatus.ACCEPTED)

# Commentaires

class CommentsListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA'],
        'POST': ['ROLE_CA']
    }
    serializer_class = RealisateurCommentSerializer
    queryset = RealisateurComment.objects.all()

class CommentsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    lookup_field = 'id'
    required_groups = {
        'GET': ['ROLE_CA'],
        'PUT': ['ROLE_CA'],
        'PATCH': ['ROLE_CA'],
        'DELETE': ['ROLE_CA']
    }
    serializer_class = RealisateurCommentSerializer
    queryset = RealisateurComment.objects.all()

# Skills

class SkillsRetrieveUpdateDestroyView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA'],
        'POST': ['ROLE_CA']
    }
    serializer_class = CompetenceSerializer
    queryset = Competence.objects.all()