from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from flower_app.controllers.permissions import HasGroupPermission, HasAnyGroupPermission
from flower_app.models.Requirement import RequirementSerializer, Requirement


class RequirementListCreateUpdateView(generics.ListCreateAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, HasAnyGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA', 'ROLE_PIOUS'],
        'POST': ['ROLE_CA', 'ROLE_PIOUS'],  # from modules/etudes/views/PhaseModifier.vue to add a phase
        'PUT': ['ROLE_CA', 'ROLE_PIOUS'],
        'PATCH': ['ROLE_CA', 'ROLE_PIOUS'],
    }
    serializer_class = RequirementSerializer
    queryset = Requirement.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='ROLE_PIOUS').exists() and not user.groups.filter(name='ROLE_CA').exists():
            # Filtrer uniquement les requirements liés à des SimuEtude
            return Requirement.objects.filter(etude__simuetude__isnull=False)
        return Requirement.objects.all()

    def update(self, request):
        print(request.data)
        serializer = RequirementSerializer(Requirement.objects.all(), data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def post(self, request):
        serializer = RequirementSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class RequirementDestroyView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, HasAnyGroupPermission]
    required_groups = {
        'DELETE': ['ROLE_CA', 'ROLE_PIOUS']
    }
    serializer_class = RequirementSerializer
    queryset = Requirement.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='ROLE_PIOUS').exists() and not user.groups.filter(name='ROLE_CA').exists():
            # Filtrer uniquement les requirements liés à des SimuEtude
            return Requirement.objects.filter(etude__simuetude__isnull=False)
        return Requirement.objects.all()