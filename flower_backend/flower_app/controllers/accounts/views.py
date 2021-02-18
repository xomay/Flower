from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
import json
from http import HTTPStatus
from rest_framework.response import Response
from rest_framework.views import APIView
from ..permissions import is_in_group, get_groups


class LoginView(APIView):
    def get(self, request):                             #from App.vue beforeCreate (so even on /login) -> redirection to login if 401
        if request.user.is_authenticated:
            return Response({
                'username': request.user.username,
                'roles': get_groups(request.user)
            }, status=HTTPStatus.ACCEPTED)
        else:
            return Response(None, status=HTTPStatus.UNAUTHORIZED)

    def post(self, request):                            #from modules/authentication/componets/AuthenticationComponent.vue : during authentication
        if not ('username' in request.data and 'password' in request.data):
            return JsonResponse({'msg': 'Bad request'})
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user is None:
            return Response(None, status=HTTPStatus.UNAUTHORIZED)
        login(request, user)
        return Response({
            'username': request.data['username'],
            'roles': get_groups(user)
        }, status=HTTPStatus.ACCEPTED)

class LogoutView(APIView):                              #from logout button (modules/navigation/Navigation.vue)
    def get(self, request):
        logout(request)
        return Response(None, status=HTTPStatus.ACCEPTED)
