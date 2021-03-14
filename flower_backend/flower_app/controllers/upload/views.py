from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
import json
from datetime import datetime
from http import HTTPStatus
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from flower_app.controllers.permissions import is_in_group, get_groups
from flower_app.models.UploadedFile import UploadedFile
from flower_app.models.People.Membre import Membre
from django.utils.encoding import smart_str

class UploadsView(APIView):
    # GET : récupérer la liste des fichiers auxquels l'utilisateur à accès.
    def get(self, request):
        if request.user.is_authenticated:
            corresponding = {}
            for u_file in UploadedFile.objects.all():
                valid = True
                for perm in u_file.permissions.all():
                    if not perm.user_set.filter(id=request.user.id).exists():
                        valid = False
                        break
                if valid:
                    corresponding[str(u_file.id)] = {
                        'id': u_file.id,
                        'displayName': u_file.displayName,
                        'size': u_file.data.size,
                        'uploadDate': u_file.uploadDate.date().strftime("%d/%m/%Y") + " " + u_file.uploadDate.time().strftime("%H/%M/%S"),
                        'author': {
                            'id': u_file.author.id,
                            'firstname': u_file.author.firstname,
                            'lastname': u_file.author.lastname,
                        }
                    }
            return Response(
                corresponding
            , status=HTTPStatus.ACCEPTED)
        else:
            return Response("Vous n'êtes pas authentifié.", status=HTTPStatus.UNAUTHORIZED)

    # POST : sauvegarder un nouveau fichier
    def post(self, request):
        if request.user.is_authenticated:
            if(request.FILES == None):
                return Response("La requête doit contenir des données dans 'request.FILES'.", status=HTTPStatus.UNAUTHORIZED)
            
            author = Membre.object.get(user=request.user)

            print(str(request.user.groups.all()))

            u_file = UploadedFile(
                author=author,
                displayName = request.data['displayName'],
                permissions = request.user.groups.all(),
                data = request.FILES['file'],
            )
            u_file.save()

            return Response({u_file.id}, status=HTTPStatus.ACCEPTED)
        else:
            return Response("Vous n'êtes pas authentifié.", status=HTTPStatus.UNAUTHORIZED)

class UploadFileView(APIView):
    def get(self, request, id):
        if request.user.is_authenticated:
            try:
                file = UploadedFile.objects.get(pk=id)
            except:
                return Response("Fichier non trouvé.", status=HTTPStatus.NOT_FOUND)
            response = HttpResponse(file.data.storage.open(file.data.name, mode='rb'), content_type='application/force-download')
            response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file.data.name.split('/')[1])
            response['X-Sendfile'] = smart_str(file.data.path)
            return response
        else:
            return Response("Vous n'êtes pas authentifié.", status=HTTPStatus.UNAUTHORIZED)
