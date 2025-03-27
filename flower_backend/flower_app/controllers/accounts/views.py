from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
import json
from http import HTTPStatus
from rest_framework.response import Response
from rest_framework.views import APIView
from ..permissions import is_in_group, get_groups
from django.http import JsonResponse
from allauth.socialaccount.models import SocialAccount



class LoginView(APIView):
    def post(self, request):
        print("Post: ", request.build_absolute_uri())  
        print("Post: ", request.headers)  

        if not request.user.is_authenticated:
            return Response({
                'error': 'Utilisateur non authentifié'
            }, status = HTTPStatus.UNAUTHORIZED)

        try:
            social_account = SocialAccount.objects.get(
                user=request.user, 
                provider='google'
            )

            user = request.user
            google_data = social_account.extra_data

            return Response({
                'user': {
                    'id': user.id,
                    'email': google_data.get('email'),
                    'name': google_data.get('name'),
                    'picture': google_data.get('picture'),
                    'is_staff': user.is_staff,
                    'is_active': user.is_active
                },
                'social_account': {
                    'uid': social_account.uid,
                    'provider': social_account.provider,
                    'last_login': social_account.last_login
                },
                'extra_data': google_data,
                'roles': get_groups(user),
            })
        
        except SocialAccount.DoesNotExist:
            return Response({
                'error': 'Compte social non trouvé'
            }, status=HTTPStatus.NOT_FOUND)
        
        except Exception as e:
            print(f"Erreur lors de la connexion : {e}")
            return Response({
                'error': 'Erreur de connexion',
                'details': str(e)
            }, status=HTTPStatus.INTERNAL_SERVER_ERROR)


class LogoutView(APIView):                              #from logout button (modules/navigation/Navigation.vue)
    def get(self, request):
        logout(request)
        return Response(None, status=HTTPStatus.ACCEPTED)
    
class Testview(APIView):
    print("TestView")
    def get(self, request):
        session_id = request.session.session_key  # Vérifier la clé de session
        user = str(request.user) if request.user.is_authenticated else "Anonymous"
        
        if not session_id:
            request.session.create()  # Forcer la création d'une session si elle n'existe pas
            session_id = request.session.session_key

        print("User:", user)
        print("Session ID:", session_id)

        return JsonResponse({"sessionid": session_id, "user": user})
