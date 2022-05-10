from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
import json
from datetime import datetime
from http import HTTPStatus
from django.http import HttpResponse, JsonResponse
from django.core.signing import Signer
from rest_framework.response import Response
from rest_framework.views import APIView
from flower_app.controllers.permissions import is_in_group, get_groups
from flower_app.models.UploadedFile import UploadedFile
from flower_app.models.People.Membre import Membre
from django.utils.encoding import smart_str
from django.conf import settings

class UploadsView(APIView):
    # GET : récupérer la liste des fichiers.
    def get(self, request):
        if request.user.is_authenticated:
            corresponding = list()
            for u_file in UploadedFile.objects.all():
                corresponding.append({
                    'id': u_file.id,
                    'displayName': u_file.displayName,
                    'size': u_file.data.size,
                    'uploadDate': u_file.uploadDate.date().strftime("%d/%m/%Y") + " " + u_file.uploadDate.time().strftime("%H:%M:%S"),
                    'author': {
                        'id': u_file.author.id,
                        'firstname': u_file.author.firstname,
                        'lastname': u_file.author.lastname,
                    }
                })
            return JsonResponse(
                corresponding
            , safe=False, status=HTTPStatus.ACCEPTED)
        else:
            return Response("Vous n'êtes pas authentifié.", status=HTTPStatus.UNAUTHORIZED)

    # POST : sauvegarder un nouveau fichier
    def post(self, request):
        if request.user.is_authenticated:
            if(request.FILES == None):
                return Response("La requête doit contenir des données dans 'request.FILES'.", status=HTTPStatus.UNAUTHORIZED)
            try:
                author = Membre.objects.get(user=request.user)
            except:
                return Response("Pour pouvoir uploader, il faut être rattaché à un utilisateur.", status=HTTPStatus.UNAUTHORIZED)

            file = UploadedFile(
                author=author,
                displayName = str(request.FILES['file']),
                uploadDate=datetime.now(),
                data = request.FILES['file'],
            )
            file.save() # save to create the primary key
            file.permissions.set(request.user.groups.all())
            file.save() # save the permissions set

            return Response({file.id}, status=HTTPStatus.ACCEPTED)
        else:
            return Response("Vous n'êtes pas authentifié.", status=HTTPStatus.UNAUTHORIZED)

class UploadFileView(APIView):
    # GET : si l'utilisateur a TOUS les droits nécessaires, on autorise le download
    def get(self, request, id):
        if request.user.is_authenticated:
            try:
                file = UploadedFile.objects.get(pk=id)
            except:
                return Response("Fichier non trouvé.", status=HTTPStatus.NOT_FOUND)
            for perm in file.permissions.all():
                if not perm.user_set.filter(id=request.user.id).exists():
                    return Response("Permission manquante : '%s'." % perm.name, status=HTTPStatus.UNAUTHORIZED)
            response = HttpResponse(file.data.storage.open(file.data.name, mode='rb'), content_type='application/force-download')
            response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file.data.name.split('/')[1])
            response['X-Sendfile'] = smart_str(file.data.path)
            return response
        else:
            return Response("Vous n'êtes pas authentifié.", status=HTTPStatus.UNAUTHORIZED)
    
    def delete(self, request, id):
        # DELETE : si l'utilisateur a TOUS les droits nécessaires, on supprime
        if request.user.is_authenticated:
            try:
                file = UploadedFile.objects.get(pk=id)
            except:
                return Response("Fichier non trouvé.", status=HTTPStatus.NOT_FOUND)
            for perm in file.permissions.all():
                if not perm.user_set.filter(id=request.user.id).exists():
                    return Response("Permission manquante : '%s'." % perm.name, status=HTTPStatus.UNAUTHORIZED)
            file.delete()
            return Response(None, status=HTTPStatus.OK)
        else:
            return Response("Vous n'êtes pas authentifié.", status=HTTPStatus.UNAUTHORIZED)

class SharedUploadFileView(APIView):
    def get(self, request, id, key):
        signer = Signer()
        expected_key = signer.sign('file'+str(id))
        if(key != expected_key):
            return HttpResponse("Invalid signature", status=HTTPStatus.FORBIDDEN)
            
        try:
            file = UploadedFile.objects.get(pk=id)
        except:
            return Response("Fichier non trouvé.", status=HTTPStatus.NOT_FOUND)
        response = HttpResponse(file.data.storage.open(file.data.name, mode='rb'), content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file.data.name.split('/')[1])
        response['X-Sendfile'] = smart_str(file.data.path)
        return response

class GetSharedUploadFilePath(APIView):
    def get(self, request, id):
        if(not request.user.is_authenticated):
            return HttpResponse(None, status=HTTPStatus.FORBIDDEN)
        signer = Signer()
        key = signer.sign('file'+str(id))
        return HttpResponse('/api/upload/'+str(id)+'/shared/'+key, status=HTTPStatus.OK)

class GetMemoryView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            mem_allowed = settings.MEMORY_UPLOAD
            mem_taken = 0
            for file in UploadedFile.objects.all():
                mem_taken += file.data.size
            mem_remain = mem_allowed - mem_taken
            return Response({
                'memoryAllowed': mem_allowed,
                'memoryTaken': mem_taken,
                'memoryRemaining': mem_remain,
            }, status=HTTPStatus.OK)
        else:
            return Response("Vous n'êtes pas authentifié.", status=HTTPStatus.UNAUTHORIZED)