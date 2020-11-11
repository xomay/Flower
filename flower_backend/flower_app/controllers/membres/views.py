from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from flower_app.controllers.permissions import HasGroupPermission
from flower_app.models.People.Membre import Membre, MembreSerializer

class MembreView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA'],                                     #from modules/etudes/components/forms/ProjectForm.vue in modules/etudes/views/EtudeModifier.vue
                                                                #   or from modules/etudes/components/forms/MissionForm.vue in modules/etudes/views/MissionCreer.vue
                                                                #   or from modules/etudes/components/forms/PVRForm.vue in modules/etudes/views/PVRCreator.vue
                                                                #   or in modules/etudes/views/PVREditor.vue or modules/membres/views/MembresVoir.vue
                                                                #   or modules/prospects/views/Devis.vue
        'POST': ['ROLE_CA'],                                    #from modules/membres/views/MembresCreer.vue
    }
    serializer_class = MembreSerializer
    queryset = Membre.objects.all()

class MembreDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    lookup_field = 'id'
    required_groups = {
        'GET': ['ROLE_CA'],                                     #from modules/membres/views/MembresDetail.vue or modules/membres/views/MembresModifier.vue
        'PUT': ['ROLE_ADMIN'],                                  #from modules/membres/views/MembresModifier.vue
        'PATCH': ['ROLE_ADMIN']
    }
    serializer_class = MembreSerializer
    queryset = Membre.objects.all()