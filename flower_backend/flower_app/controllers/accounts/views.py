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
    def post(self, request):
        print("Post: ", request.build_absolute_uri())  # Debugging info
        print("Post: ", request.headers)  # Debugging info
        try:
            # Adapter GoogleOAuth2 pour récupérer l'utilisateur à partir du token
            google_adapter = GoogleOAuth2Adapter()
            sociallogin = SocialLogin(adapter=google_adapter)

            # Compléter le login avec le token reçu
            sociallogin.token = token
            complete_social_login(request, sociallogin)

            # Si l'utilisateur est authentifié
            if sociallogin.is_authenticated:
                # Assigner le backend d'authentification
                request.user.backend = 'allauth.account.auth_backends.AuthenticationBackend'

                # Se connecter avec l'utilisateur
                perform_login(request, sociallogin.user, post_save=True)

                # Réponse avec les informations utilisateur
                return Response({
                    'username': sociallogin.user.username,
                    'roles': get_groups(sociallogin.user)
                }, status=HTTPStatus.ACCEPTED)
            else:
                return Response({"msg": "Authentification échouée avec Google"}, status=HTTPStatus.UNAUTHORIZED)

        except OAuth2Error as e:
            # Si une erreur OAuth se produit, renvoyer un message d'erreur
            return Response({"msg": "Erreur OAuth avec Google", "error": str(e)}, status=HTTPStatus.BAD_REQUEST)
        except Exception as e:
            # Attraper toute autre erreur et la renvoyer
            return Response({"msg": "Erreur inattendue", "error": str(e)}, status=HTTPStatus.INTERNAL_SERVER_ERROR)


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
