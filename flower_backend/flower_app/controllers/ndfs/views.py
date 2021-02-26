from rest_framework.response import Response
from rest_framework.views import APIView
from http import HTTPStatus
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from flower_app.controllers.permissions import HasGroupPermission
from flower_app.models.NdF import NdF, NdFSerializer
from flower_app.models.NdFDetail import NdFDetail
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
    
    # Durant le POST, on remplace les ID de contactway par leur valeur textuelle.
    def create(self, *args, **kwargs):
        data = args[0].data
        print("Create instance")
        demandeur = Membre.objects.get(pk=data['demandeur'])
        instance = NdF(
            demandeur=demandeur,
            date=data['date'],
            objet=data['objet'],
            mandat=data['mandat'],
            numberThisYear=data['numberThisYear']
        )
        instance.save()
        print("Created the instance. Id="+str(instance.id))
        for detail in data["details"]:
            print("Create "+detail['description'])
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
            print("> Created " + str(detail_instance))
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
