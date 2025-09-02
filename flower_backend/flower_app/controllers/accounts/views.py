from django.contrib.auth.models import Group
from django.http import JsonResponse
from django.contrib.auth import login, logout
from django.views import View
from http import HTTPStatus
from flower_app.models.People.Membre import Membre, Poste
from rest_framework.response import Response
from rest_framework.views import APIView
from ..permissions import get_groups
from django.http import JsonResponse
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter

class LoginView(APIView):
    def post(self, request):
        print("Post: ", request.build_absolute_uri())  

        print("Request" + str(request))
        print("UID" + str(request.data.get('uid')))

        poste = ""

        if not request.user.is_authenticated:
            try:
                social_account = SocialAccount.objects.get(
                    uid=request.data.get('uid'), 
                    provider='google'
                )
                
                user = social_account.user
                login(request, user)
                
            except SocialAccount.DoesNotExist:
                return Response({
                    'error': 'Utilisateur non trouvé ou non autorisé'
                }, status=HTTPStatus.UNAUTHORIZED)

        print(f"User: {request.user}")

        try:
            social_account = SocialAccount.objects.get(
                user=request.user, 
                provider='google'
            )

            user = request.user
            google_data = social_account.extra_data

            try: 
                membre = Membre.objects.get(user=user)
                poste = Poste.objects.get(membre=membre)
                poste_groups = Group.objects.filter(poste=poste)
                user.groups.set(poste_groups)
            except Membre.DoesNotExist:  # Si aucun Membre associé à l'utilisateur
                try:
                    if user.id == '' or not user.id:  # Important : forcer la sauvegarde du User avant de l'associer
                        user.save()

                    membre = Membre.objects.get(email_junior=google_data.get('email'))
                    membre.user = user
                    membre.save()
                    poste = Poste.objects.get(membre=membre)
                    poste_groups = Group.objects.filter(poste=poste)
                    user.groups.set(poste_groups)
                except Membre.DoesNotExist:
                    print("Aucun membre trouvé avec cet email")
                    membre = None  # Assigner une valeur par défaut pour éviter les erreurs
                except Poste.DoesNotExist:
                    print("Ce poste n'existe pas")
                    poste = None

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
                'roles': get_groups(poste),
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
