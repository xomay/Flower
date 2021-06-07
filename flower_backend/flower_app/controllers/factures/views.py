from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.http import HttpResponse
from datetime import datetime
from http import HTTPStatus
from flower_app.controllers.permissions import HasGroupPermission
from flower_app.models.Facture import Facture, FactureSerializer
from flower_app.models.FactureDetail import FactureDetail, FactureDetailSerializer

class FactureView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA', 'ROLE_TRESO'],
        'POST': ['ROLE_CA', 'ROLE_TRESO']                             #from modules/etudes/views/invoice/InvoiceCreate.vue
    }
    serializer_class = FactureSerializer
    queryset = Facture.objects.all()

# Renvoie, le nombre de facture ayant été produites ce mois-ci.
class GetMonthAmount(APIView):
    def get(self, request):
        if(not request.user.is_authenticated):
            return HttpResponse(None, status=HTTPStatus.FORBIDDEN)
        year = str(datetime.now().year)[-2:]
        month = str(datetime.now().month)[-2:]
        real = "FA" + ("0" + year, year)[int(year) > 10] + ("0" + month, month)[int(month) > 10]
        compteur = 0
        for facture in Facture.objects.all():
            if(facture.invoiceNumber[:6] == real):
                compteur = compteur + 1
        return HttpResponse(compteur, status=HTTPStatus.OK)

class FactureLineView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA', 'ROLE_TRESO'],                             #from modules/etudes/views/invoice/InvoiceModify.vue
        'PUT': ['ROLE_CA', 'ROLE_TRESO'],                             #from modules/etudes/views/invoice/InvoiceModify.vue
        'PATCH': ['ROLE_CA', 'ROLE_TRESO'],
        'DELETE': ['ROLE_CA', 'ROLE_TRESO']
    }
    serializer_class = FactureSerializer
    queryset = Facture.objects.all()

    def update(self, request, pk):
        serializer = FactureSerializer(instance=Facture.objects.get(id=pk),data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(request.data)

class RemoveFactureLineView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'DELETE': ['ROLE_CA', 'ROLE_TRESO']
    }
    serializer_class = FactureDetailSerializer
    queryset = FactureDetail.objects.all()
