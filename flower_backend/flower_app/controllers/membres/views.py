from django.contrib.auth.models import User, Group

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from http import HTTPStatus
import random, string

from flower_app.controllers.permissions import HasGroupPermission
from flower_app.models.People.Membre import Membre, MembreSerializer
from flower_app.models.Poste import Poste
from flower_app.email.mail_user_accounts import send_mail_user_account_creation

class MembreView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA'],
        'POST': ['ROLE_CA'],
    }
    serializer_class = MembreSerializer
    queryset = Membre.objects.all()

    def post(self, request):
        rep = super().post(request)
        new_membre = Membre.objects.get(pk=rep.data['id'])
        new_membre.poste = Poste.objects.get(pk=request.data['poste'])
        new_membre.save()
        serializer = MembreSerializer(new_membre)
        return Response(serializer.data, status=HTTPStatus.CREATED)

class MembreDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA'],
        'PUT': ['ROLE_ADMIN'],
        'PATCH': ['ROLE_ADMIN']
    }
    serializer_class = MembreSerializer
    queryset = Membre.objects.all()

    # J'ai été obligé de me compliquer la vie ici, pour une raison que j'ignore :/
    def update(self, *args, **kwargs):
        data = args[0].data
        response = super().update(*args, **kwargs)
        membre = Membre.objects.get(pk=kwargs['pk'])
        membre.poste = Poste.objects.get(pk=data['poste'])
        membre.save()
        serializer = MembreSerializer(membre)
        return Response(serializer.data, status=HTTPStatus.OK)

class OpenAccountView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'PUT': ['ROLE_ADMIN'],
    }
    serializer_class = MembreSerializer
    queryset = Membre.objects.all()
    def update(self, request, pk):
        membre = Membre.objects.get(id=pk)
        new_username = "{firstname}.{lastname}".format(firstname=membre.firstname, lastname=membre.lastname).replace(" ", "").lower()
        new_password = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(16))
        print("new username >"+new_username)
        print("new password >"+new_password)
        newAccount = User(
            username=new_username,
            password=new_password
        )
        newAccount.save()
        membre.user = newAccount
        membre.save()
        groupCA = Group.objects.get(name='ROLE_CA') 
        groupCA.user_set.add(newAccount)
        try:
            print("Send mail to new user.")
            send_mail_user_account_creation(membre, new_username, new_password)
        except Exception as e:
            print("Impossible d'envoyer l'email : " +str(e))
        return Response(data={"username": newAccount.username}, status=HTTPStatus.CREATED)
