from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from flower_app.controllers.permissions import HasGroupPermission, is_in_group
from flower_app.models.Facture import Facture, FactureSerializer
from flower_app.models.FactureDetail import FactureDetail, FactureDetailSerializer
from flower_app.models.Etude import Etude

class FactureView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA', 'ROLE_TRESO'],
        'POST': ['ROLE_CA', 'ROLE_TRESO']                             #from modules/etudes/views/invoice/InvoiceCreate.vue
    }
    serializer_class = FactureSerializer
    queryset = Facture.objects.all()

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
        'DELETE': ['ROLE_CA', 'ROLE_TRESO']                                   #from modules/etudes/components/invoice/InvoiceForm.vue in modules/etudes/views/invoice/InvoiceCreate.vue
                                                                #   or in modules/etudes/views/invoice/InvoiceModify.vue
    }
    serializer_class = FactureDetailSerializer
    queryset = FactureDetail.objects.all()
