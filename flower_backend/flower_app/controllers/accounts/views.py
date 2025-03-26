from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
import json
from http import HTTPStatus
from rest_framework.response import Response
from rest_framework.views import APIView
from ..permissions import is_in_group, get_groups
from django.http import JsonResponse


class LoginView(APIView):
    print("LoginView------------------------------------------------")
    def get(self, request):  
        print("Get: ", request.build_absolute_uri())                           #from App.vue beforeCreate (so even on /login) -> redirection to login if 401
        print("Get: ", request.headers)                           #from App.vue beforeCreate (so even on /login) -> redirection to login if 401
        if request.user.is_authenticated:
            return Response({
                'username': request.user.username,
                'roles': get_groups(request.user)
            }, status=HTTPStatus.ACCEPTED)
        else:
            print(request.user)
            return Response(None, status=HTTPStatus.UNAUTHORIZED)

    def post(self, request):   
        print("Post : ", request)                         #from modules/authentication/componets/AuthenticationComponent.vue : during authentication
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
    
class Testview(APIView):
    def get(self, request):
        session_id = request.session.session_key  # Vérifier la clé de session
        user = str(request.user) if request.user.is_authenticated else "Anonymous"
        
        if not session_id:
            request.session.create()  # Forcer la création d'une session si elle n'existe pas
            session_id = request.session.session_key

        print("User:", user)
        print("Session ID:", session_id)

        return JsonResponse({"sessionid": session_id, "user": user})
