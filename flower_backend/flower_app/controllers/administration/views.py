import os
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from http import HTTPStatus
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.shortcuts import get_object_or_404
from flower_app.controllers.permissions import is_in_group
from flower_app.controllers.permissions import HasGroupPermission
from flower_app.models.ParamsJE import ParamsJE, ParamsJESerializer
from flower_app.models.Poste import Poste, PosteSerializer
from flower_app.models.BaseUrsaff import BaseUrsaff, BaseUrsaffSerializer, getLastBase
from django.core.files.storage import FileSystemStorage


# Paramètres généraux

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

class GetParameter(APIView):
    def get(self, request, requ):
        try:
            params = ParamsJE.objects.get(pk=1)
            try:
                data_found = getattr(params, requ)
                return Response({data_found}, status=HTTPStatus.ACCEPTED)
            except:
                return Response({"Donnée ("+requ+") indéfinie."}, status=HTTPStatus.SERVICE_UNAVAILABLE)
        except:
            return Response({"Il faut initialiser les paramètres de la JE !"}, status=HTTPStatus.NOT_FOUND)

# Postes

class PostesCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA'],
        'POST': ['ROLE_ADMIN']
    }
    serializer_class = PosteSerializer
    queryset = Poste.objects.all()

class PostesUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA'],
        'PUT': ['ROLE_ADMIN'],
        'PATCH': ['ROLE_ADMIN'],
        'DELETE': ['ROLE_ADMIN']
    }
    serializer_class = PosteSerializer
    queryset = Poste.objects.all()

# Base Ursaff

class BaseUrsaffView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA'],
        'POST': ['ROLE_CA', 'ROLE_TRESO']
    }
    serializer_class = BaseUrsaffSerializer
    queryset = BaseUrsaff.objects.all()

class BaseUrsaffDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA'],
        'PUT': ['ROLE_CA', 'ROLE_TRESO'],
        'PATCH': ['ROLE_CA', 'ROLE_TRESO'],
        'DELETE': ['ROLE_CA', 'ROLE_TRESO']
    }
    serializer_class = BaseUrsaffSerializer
    queryset = BaseUrsaff.objects.all()

class BaseUrsaffLastView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            if is_in_group(request.user, 'ROLE_TRESO'):
                serializer = BaseUrsaffSerializer(getLastBase(), read_only=True)
                return JsonResponse(serializer.data, status=HTTPStatus.OK)
        return Response(None, status=HTTPStatus.FORBIDDEN)
    

class DoctypeImportView(APIView):
    def post(self, request, title):
        print(request.FILES)
        print(title)
        if request.FILES:
            uploaded_file = request.FILES["file"]
            print(uploaded_file)
            print("cwd : "+ os.getcwd())
            save_path = os.path.abspath(os.path.join(os.getcwd(), "doctypes"))
            print(save_path)

            # Vérifier si le dossier existe, sinon le créer
            if not os.path.exists(save_path):
                os.makedirs(save_path)

            # Enregistrer le fichier
            file_storage = FileSystemStorage(location=save_path)
            print(file_storage)
            file_name = file_storage.save(title, uploaded_file)

            return Response({"message": "Fichier uploadé avec succès", "file_path": file_name}, status=HTTPStatus.OK)
        
        return Response({"error": "Aucun fichier reçu"}, status=HTTPStatus.BAD_REQUEST)