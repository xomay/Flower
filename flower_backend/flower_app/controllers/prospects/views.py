from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from flower_app.controllers.permissions import HasGroupPermission
from flower_app.models.People.Prospect import Prospect, ProspectSerializer
from flower_app.models.People.Employe import Employe, EmployeSerializer
from flower_app.models.Prospection import ContactWay

class ProspectListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA'],                                         #from modules/etudes/components/forms/ProjectForm.vue in modules/etudes/views/EtudeModifier.vue
                                                                    #   or modules/etudes/views/invoice/InvoiceCreate.vue or modules/etudes/views/invoice/InvoiceModify.vue
                                                                    #   or modules/prospects/views/ProspectsVoir.vue
        'POST': ['ROLE_CA']                                         #from modules/prospects/views/ProspectsCreer.vue
    }
    serializer_class = ProspectSerializer
    queryset = Prospect.objects.all()

# Méthode pour remplacer un l'array d'ids par les valeurs textuelles qui leur sont associés. 
def remplaceContactsIdByValue(response):
    if "contactWay" in response.data:
        ctts = []
        for contactID in response.data["contactWay"]:
            ctts.append(ContactWay.objects.get(pk=contactID).__str__())
        response.data["contactWay"] = ctts
    return response

class ProspectRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA'],                                         #from modules/prospects/views/ProspectsDetail.vue or modules/prospects/views/ProspectsModifier.vue
        'PUT': ['ROLE_CA'],                                         #from modules/prospects/views/ProspectsDetail.vue (unused) or modules/prospects/views/ProspectsModifier.vue
        'PATCH': ['ROLE_CA'],
        'DELETE': ['ROLE_CA']                                       #from modules/prospects/views/ProspectsModifier.vue
    }
    serializer_class = ProspectSerializer
    queryset = Prospect.objects.all()

    # Durant le GET, on update en fct des stings PUIS on remplace les ID de contactway par leur valeur textuelle.
    def update(self, *args, **kwargs):
        data = args[0].data
        if "contactWay" in data:
            realRequest = []
            for contactStr in data["contactWay"]:
                try:
                    # Le contact existe déjà : on le récupère
                    found = ContactWay.objects.get(contactWay=contactStr)
                    realRequest.append(found.id)
                except:
                    # Le contact n'existe pas : on le créer
                    contact = ContactWay(contactWay=contactStr)
                    contact.save()
                    realRequest.append(contact.id)
            args[0].data["contactWay"] = realRequest
        return remplaceContactsIdByValue(super().update(*args, **kwargs))
    
    # Durant le POST, on remplace les ID de contactway par leur valeur textuelle.
    def create(self, *args, **kwargs):
        response = super().create(*args, **kwargs)
        return remplaceContactsIdByValue(response)
    
    # Durant le GET, on remplace les ID de contactway par leur valeur textuelle.
    def get(self, *args, **kwargs):
        response = super().get(*args, **kwargs)
        return remplaceContactsIdByValue(response)

class EmployeListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA'],                                         #from modules/etudes/components/forms/PVRForm.vue in modules/etudes/views/PVRCreator.vue
                                                                    #   or in modules/etudes/views/PVREditor.vue or from modules/prospects/views/ProspectsDetail.vue
                                                                    #   or modules/prospects/views/ProspectsModifier.vue
        'POST': ['ROLE_CA']                                         #from modules/prospects/views/EmployesCreer.vue
    }
    serializer_class = EmployeSerializer
    def get_queryset(self):
        prospectId = self.kwargs.get('id')
        # Searching employees from a prospect
        employes = Prospect.objects.get(id=prospectId).employe_set
        return employes
    
    def create(self, request, id):
        request.data['prospect'] = id
        return super().create(request)

class EmployeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA'],                                         #from modules/prospects/views/EmployesModifier.vue or modules/prospects/views/EmployesDetail.vue
        'PUT': ['ROLE_CA'],                                         #from modules/prospects/views/EmployesModifier.vue
        'PATCH': ['ROLE_CA'],
        'DELETE': ['ROLE_CA']                                       #from modules/prospects/views/EmployesModifier.vue
    }
    serializer_class = EmployeSerializer
    queryset = Employe.objects.all()
    lookup_field = 'id'
