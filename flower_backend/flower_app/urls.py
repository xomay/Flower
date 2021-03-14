from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

urlpatterns = [
    path('etudes/', include('flower_app.controllers.etudes.urls')),
    path('etudes/groupes/', include('flower_app.controllers.groupes.urls')),
    path('etudes/phases/', include('flower_app.controllers.phases.urls')),
    path('etudes/uss/', include('flower_app.controllers.uss.urls')),
    path('tresorerie/factures/', include('flower_app.controllers.factures.urls')),
    path('membres/', include('flower_app.controllers.membres.urls')),
    path('accounts/', include('flower_app.controllers.accounts.urls')),
    path('prospects/', include('flower_app.controllers.prospects.urls')),
    path('publish/', include('flower_app.controllers.publishing.urls')),
    path('gantt/', include('flower_app.controllers.gantt.urls')),
    path('pvr/', include('flower_app.controllers.pvr.urls')),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('actioncom/', include('flower_app.controllers.actioncom.urls')),
    path('contactway/', include('flower_app.controllers.contactway.urls')),
    path('realisateurs/', include('flower_app.controllers.realisateurs.urls')),
    path('administration/', include('flower_app.controllers.administration.urls')),
    path('ndfs/', include('flower_app.controllers.ndfs.urls')),
    path('ndfs/details/', include('flower_app.controllers.ndfsdetails.urls')),
    path('upload/', include('flower_app.controllers.upload.urls')),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]