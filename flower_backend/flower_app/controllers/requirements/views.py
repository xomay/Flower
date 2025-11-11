from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from flower_app.controllers.permissions import HasGroupPermission
from flower_app.models.Requirement import RequirementSerializer, Requirement


class RequirementListCreateUpdateView(generics.ListCreateAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA'],
        'POST': ['ROLE_CA'],  # from modules/etudes/views/PhaseModifier.vue to add a phase
        'PUT': ['ROLE_CA'],
        'PATCH': ['ROLE_CA'],
    }
    serializer_class = RequirementSerializer
    queryset = Requirement.objects.all()

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
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'DELETE': ['ROLE_CA']
    }
    serializer_class = RequirementSerializer
    queryset = Requirement.objects.all()