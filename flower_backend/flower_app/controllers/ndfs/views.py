from rest_framework.response import Response
from rest_framework.views import APIView
from http import HTTPStatus
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from flower_app.controllers.permissions import HasGroupPermission
from flower_app.models.NdF import NdF, NdFSerializer
from flower_app.models.NdFDetail import NdFDetail
from flower_app.models.UploadedFile import UploadedFile
from flower_app.models.People.Membre import Membre

class NFListView(generics.ListCreateAPIView, generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA', 'ROLE_TRESO'],
        'POST': ['ROLE_CA', 'ROLE_TRESO'],
        'PUT': ['ROLE_CA', 'ROLE_TRESO'],
        'PATCH': ['ROLE_CA', 'ROLE_TRESO']
    }
    serializer_class = NdFSerializer
    queryset = NdF.objects.all()
    
    def update(self, request):
        serializer = NdFSerializer(NdF.objects.all(), data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def create(self, *args, **kwargs):
        data = args[0].data
        demandeur = Membre.objects.get(pk=data['demandeur'])
        howManyThisYear = len(NdF.objects.filter(mandat=data['mandat'])) + 1
        instance = NdF(
            demandeur=demandeur,
            date=data['date'],
            objet=data['objet'],
            mandat=data['mandat'],
            numberThisYear=howManyThisYear
        )
        instance.save()
        for detail in data["details"]:
            detail_instance = NdFDetail(
                ndf=instance,
                index=detail['index'],
                description=detail['description'],
                detailType=detail['detailType'],
                prixHT=detail['prixHT'],
                tva=detail['tva'],
                nbKilometres=detail['nbKilometres'],
                prixCentimesKilometres=detail['prixCentimesKilometres']
            )
            detail_instance.save()
        return Response(instance.id, status=HTTPStatus.ACCEPTED)

class NFRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA', 'ROLE_TRESO'],
        'PUT': ['ROLE_CA', 'ROLE_TRESO'],
        'PATCH': ['ROLE_CA', 'ROLE_TRESO'],
        'DELETE': ['ROLE_CA', 'ROLE_TRESO']
    }
    serializer_class = NdFSerializer
    queryset = NdF.objects.all()

class NFEditFiles(APIView):
    def put(self, request, id):
        if not request.user.is_authenticated:
            return Response("You are not authenticated.", status=HTTPStatus.UNAUTHORIZED)
        ndf = NdF.objects.get(pk=id)
        file = UploadedFile.objects.get(pk=request.data['new_file'])
        ndf.linkedFiles.add(file)
        ndf.save()
        return Response(None, status=HTTPStatus.OK)
