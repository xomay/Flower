from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.http import HttpResponse
from django.core.signing import Signer
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

def getFacturesAmountInMonth(year, month):
    # On met au format "FA" + <yyMM>
    real = "FA" + year + month
    compteur = 0
    for facture in Facture.objects.all():
        if(facture.invoiceNumber[:6] == real):
            compteur = compteur + 1
    return compteur

# Renvoie, le nombre de facture ayant été produites ce mois-ci.
class GetMonthAmount(APIView):
    def get(self, request):
        if(not request.user.is_authenticated):
            return HttpResponse(None, status=HTTPStatus.FORBIDDEN)
        year = str(datetime.now().year)[-2:]
        month = str(datetime.now().month)[-2:]
        year = ("0" + year, year)[int(year) > 9]
        month = ("0" + month, month)[int(month) > 9]
        return HttpResponse(getFacturesAmountInMonth(year, month), status=HTTPStatus.OK)

class GetMonthAmountSel(APIView):
    def get(self, request, dateSelector):
        if(not request.user.is_authenticated):
            return HttpResponse(None, status=HTTPStatus.FORBIDDEN)
        year = dateSelector[2:4]
        month = dateSelector[-2:]
        return HttpResponse(getFacturesAmountInMonth(year, month), status=HTTPStatus.OK)

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

class GetSharedFacturePath(APIView):
    def get(self, request, facture_id):
        if(not request.user.is_authenticated):
            return HttpResponse(None, status=HTTPStatus.FORBIDDEN)
        signer = Signer()
        key = signer.sign('facture'+str(facture_id))
        return HttpResponse('/api/publish/facture/1/shared/'+key, status=HTTPStatus.OK)