from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from http import HTTPStatus
import random
import string
from django.contrib.auth.models import User, Group

from flower_app.controllers.permissions import HasGroupPermission, HasAnyGroupPermission
from flower_app.models.People.Realisateur import Realisateur, RealisateurSerializer, RealisateurComment, \
    RealisateurCommentSerializer, SimuRealisateur
from flower_app.models.Competence import Competence, CompetenceSerializer

from flower_app.email.mail_reas_accounts import send_mail_rea_account_creation, send_mail_rea_account_deletion

# Réalisateur

class RealisateurListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, HasAnyGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA', 'ROLE_PIOUS'],                                         #
        'POST': ['ROLE_CA', 'ROLE_PIOUS']                                         #
    }
    serializer_class = RealisateurSerializer
    queryset = Realisateur.objects.filter(simurealisateur__isnull=False)

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='ROLE_PIOUS').exists() and not user.groups.filter(
                name='ROLE_CA').exists():
            return SimuRealisateur.objects.all()
        else:
            return Realisateur.objects.filter(simurealisateur__isnull=True)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not self.request.user.groups.filter(name__in=['ROLE_PIOUS','ROLE_CA']).exists():
            return Response({"detail": "Vous n'avez pas la permission d'accéder à cette ressource."}, status=HTTPStatus.FORBIDDEN)

        # Extraire les champs many-to-many
        validated_data = serializer.validated_data
        skills = validated_data.pop('skills', [])
        comments = validated_data.pop('comments', [])

        if self.request.user.groups.filter(name='ROLE_PIOUS').exists() and not self.request.user.groups.filter(
            name='ROLE_CA').exists():
            new_realisateur = SimuRealisateur.objects.create(**validated_data)
        else:
            new_realisateur = Realisateur.objects.create(**validated_data)

        # Assigner les champs many-to-many
        if skills:
            new_realisateur.skills.set(skills)
        if comments:
            new_realisateur.comments.set(comments)

        serializer = RealisateurSerializer(new_realisateur)
        return Response(serializer.data, status=HTTPStatus.CREATED)

class RealisateurRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, HasAnyGroupPermission]
    lookup_field = 'id'
    required_groups = {
        'GET': ['ROLE_CA', 'ROLE_PIOUS'],
        'PUT': ['ROLE_CA', 'ROLE_PIOUS'],
        'PATCH': ['ROLE_CA', 'ROLE_PIOUS'],
        'DELETE': ['ROLE_CA', 'ROLE_PIOUS']
    }
    serializer_class = RealisateurSerializer
    #queryset = Realisateur.objects.all()

    def get_queryset(self):
        if self.request.user.groups.filter(name='ROLE_PIOUS').exists() and not self.request.user.groups.filter(
            name='ROLE_CA').exists():
            return SimuRealisateur.objects.all()
        return Realisateur.objects.filter(simurealisateur__isnull=True)

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
        print(">"+new_username)
        print(">"+new_password)
        newAccount = User.objects.create_user(
            username=new_username,
            email=realisateur.email_insa,
            password=new_password
        )
        newAccount.set_password(new_password)
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
    permission_classes = [IsAuthenticated, HasAnyGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA', 'ROLE_PIOUS'],
        'POST': ['ROLE_CA', 'ROLE_PIOUS']
    }
    serializer_class = RealisateurCommentSerializer
    queryset = RealisateurComment.objects.all()

class CommentsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, HasAnyGroupPermission]
    lookup_field = 'id'
    required_groups = {
        'GET': ['ROLE_CA', 'ROLE_PIOUS'],
        'PUT': ['ROLE_CA', 'ROLE_PIOUS'],
        'PATCH': ['ROLE_CA', 'ROLE_PIOUS'],
        'DELETE': ['ROLE_CA', 'ROLE_PIOUS']
    }
    serializer_class = RealisateurCommentSerializer
    queryset = RealisateurComment.objects.all()

# Skills

class SkillsRetrieveUpdateDestroyView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, HasAnyGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA', 'ROLE_PIOUS'],
        'POST': ['ROLE_CA', 'ROLE_PIOUS']
    }
    serializer_class = CompetenceSerializer
    queryset = Competence.objects.all()
