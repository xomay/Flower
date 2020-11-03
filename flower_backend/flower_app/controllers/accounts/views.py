from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout

from http import HTTPStatus
from rest_framework.response import Response
from rest_framework.views import APIView

class LoginView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return Response(None, status=HTTPStatus.ACCEPTED)
        else:
            return Response(None, status=HTTPStatus.UNAUTHORIZED)

    def post(self, request):
        if not ('username' in request.data and 'password' in request.data):
            return JsonResponse({'msg': 'Bad request'})
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user is not None:
            login(request, user)
            return Response(None, status=HTTPStatus.ACCEPTED)
        else:
            return Response(None, status=HTTPStatus.UNAUTHORIZED)

class LogoutView(APIView): 
    def get(self, request):
        logout(request)
        return Response(None, status=HTTPStatus.ACCEPTED)
