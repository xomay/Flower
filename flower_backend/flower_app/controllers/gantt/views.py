from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from flower_app.controllers.permissions import HasGroupPermission
from .gantt import computeGanttFromEtude
from flower_app.models.Etude import Etude

class GanttView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA']                                      #from modules/etudes/components/Summary.vue
    }

    def retrieve(self, request, etude_id):
        etude = Etude.objects.get(pk=etude_id)
        return computeGanttFromEtude(etude, image_format=self.request.query_params.get('type', 'jpg'))

