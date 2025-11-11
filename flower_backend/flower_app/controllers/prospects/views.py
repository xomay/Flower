from http import HTTPStatus

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from flower_app.controllers.permissions import HasGroupPermission, HasAnyGroupPermission
from flower_app.models.People.Prospect import Prospect, ProspectSerializer, SimuProspect
from flower_app.models.People.Employe import Employe, EmployeSerializer
from flower_app.models.Prospection import ContactWay

# Méthode pour remplacer un l'array d'ids par les valeurs textuelles qui leur sont associés. 
def remplaceContactsIdByValue(response):
    if "contactWay" in response.data:
        ctts = []
        for contactID in response.data["contactWay"]:
            ctts.append(ContactWay.objects.get(pk=contactID).__str__())
        response.data["contactWay"] = ctts
    return response

class ProspectListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, HasAnyGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA', 'ROLE_PIOUS'],                                         #from modules/etudes/components/forms/ProjectForm.vue in modules/etudes/views/EtudeModifier.vue
                                                                    #   or modules/etudes/views/invoice/InvoiceCreate.vue or modules/etudes/views/invoice/InvoiceModify.vue
                                                                    #   or modules/prospects/views/ProspectsVoir.vue
        'POST': ['ROLE_CA', 'ROLE_PIOUS']                                         #from modules/prospects/views/ProspectsCreer.vue
    }
    serializer_class = ProspectSerializer
    queryset = Prospect.objects.all()

    def get(self, request):
        user = self.request.user
        if not user.groups.filter(name__in=['ROLE_PIOUS','ROLE_CA']).exists():
            return Response({"detail": "Vous n'avez pas la permission d'accéder à cette ressource."}, status=HTTPStatus.FORBIDDEN)
        elif user.groups.filter(name='ROLE_PIOUS').exists() and not user.groups.filter(name='ROLE_CA').exists():
            self.queryset = SimuProspect.objects.all()
            return super().get(self)
        return super().get(self)

    # Durant le POST, on remplace les ID de contactway par leur valeur textuelle.
    def create(self, request, *args, **kwargs):
        #data = args[0].data
        data = request.data.copy()
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
            #args[0].data["contactWay"] = realRequest
            data.pop("contactWay")

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user

        if not user.groups.filter(name__in=['ROLE_PIOUS', 'ROLE_CA']).exists():
            return Response({"detail": "Vous n'avez pas la permission d'accéder à cette ressource."},
                            status=HTTPStatus.FORBIDDEN)
        if user.groups.filter(name='ROLE_PIOUS').exists() and not user.groups.filter(
                name='ROLE_CA').exists():
            new_prospect = SimuProspect.objects.create(**serializer.validated_data)
        else:
            new_prospect = Prospect.objects.create(**serializer.validated_data)

        if realRequest:
            new_prospect.contactWay.set(realRequest)

        serializer = ProspectSerializer(new_prospect)
        #return remplaceContactsIdByValue(super().create(*args, **kwargs))
        return Response(remplaceContactsIdByValue(serializer).data, status=HTTPStatus.CREATED)
class ProspectRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, HasAnyGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA', 'ROLE_PIOUS'],                                         #from modules/prospects/views/ProspectsDetail.vue or modules/prospects/views/ProspectsModifier.vue
        'PUT': ['ROLE_CA', 'ROLE_PIOUS'],                                         #from modules/prospects/views/ProspectsDetail.vue (unused) or modules/prospects/views/ProspectsModifier.vue
        'PATCH': ['ROLE_CA', 'ROLE_PIOUS'],
        'DELETE': ['ROLE_CA', 'ROLE_PIOUS']                                       #from modules/prospects/views/ProspectsModifier.vue
    }
    serializer_class = ProspectSerializer
    queryset = Prospect.objects.all()

    def get_queryset(self):
        if self.request.user.groups.filter(name='ROLE_PIOUS').exists() and not self.request.user.groups.filter(
            name='ROLE_CA').exists():
            return SimuProspect.objects.all()
        return Prospect.objects.filter(simuprospect__isnull=True)

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
    
    # Durant le GET, on remplace les ID de contactway par leur valeur textuelle.
    def get(self, *args, **kwargs):
        response = super().get(*args, **kwargs)
        return remplaceContactsIdByValue(response)

class EmployeListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, HasAnyGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA', 'ROLE_PIOUS'],                                         #from modules/etudes/components/forms/PVRForm.vue in modules/etudes/views/PVRCreator.vue
                                                                    #   or in modules/etudes/views/PVREditor.vue or from modules/prospects/views/ProspectsDetail.vue
                                                                    #   or modules/prospects/views/ProspectsModifier.vue
        'POST': ['ROLE_CA', 'ROLE_PIOUS']                                         #from modules/prospects/views/EmployesCreer.vue
    }
    serializer_class = EmployeSerializer
    def get_queryset(self):
        prospectId = self.kwargs.get('id')
        # Searching employees from a prospect
        if self.request.user.groups.filter(name='ROLE_PIOUS').exists() and not self.request.user.groups.filter(
            name='ROLE_CA').exists():
            employes = SimuProspect.objects.get(id=prospectId).employe_set
        else:
            employes = Prospect.objects.get(id=prospectId).employe_set
        return employes
    
    def create(self, request, id):
        request.data['prospect'] = id
        return super().create(request)

class EmployeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, HasAnyGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA', 'ROLE_PIOUS'],                                         #from modules/prospects/views/EmployesModifier.vue or modules/prospects/views/EmployesDetail.vue
        'PUT': ['ROLE_CA', 'ROLE_PIOUS'],                                         #from modules/prospects/views/EmployesModifier.vue
        'PATCH': ['ROLE_CA', 'ROLE_PIOUS'],
        'DELETE': ['ROLE_CA', 'ROLE_PIOUS']                                       #from modules/prospects/views/EmployesModifier.vue
    }
    serializer_class = EmployeSerializer
    queryset = Employe.objects.all()
    lookup_field = 'id'
