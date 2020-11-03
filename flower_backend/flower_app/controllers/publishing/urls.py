from django.urls import include, path
from . import views

urlpatterns = [
    path('etude/<int:etude_id>/devis/', views.DevisView.as_view()),
    path('etude/<int:etude_id>/ce/', views.CEView.as_view()),
    path('facture/<int:facture_id>/', views.FactureView.as_view()),
    path('pvr/<int:pvr_id>/', views.PVRView.as_view()),
    path('rdm/<int:rdm_id>/', views.RDMView.as_view()),
    path('devis/', views.CustomDevisView.as_view())
]