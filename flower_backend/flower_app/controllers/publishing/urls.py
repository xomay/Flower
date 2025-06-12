from django.urls import include, path
from . import views

#Base url for here is '/publish/'

urlpatterns = [
    path('etude/<int:etude_id>/devis/', views.DevisView.as_view()),
    path('etude/<int:etude_id>/ce/doc/', views.CEViewDocx.as_view()),
    path('etude/<int:etude_id>/ce/pdf/', views.CEViewPdf.as_view()),
    path('facture/<int:facture_id>/', views.FactureView.as_view()),
    path('facture/<int:facture_id>/shared/<str:key>', views.SharedFactureView.as_view()),
    path('pvr/<int:pvr_id>/', views.PVRView.as_view()),
    path('rdm/<int:rdm_id>/', views.RDMView.as_view()),
    path('ndf/<int:ndf_id>/', views.NdFView.as_view()),
    path('bv/<int:bv_id>/', views.BVView.as_view()),
    path('ba/<int:etudiant_id>', views.BAView.as_view()),
    path('barea/<int:etudiant_id>', views.BAReaView.as_view()),
    path('devis/', views.CustomDevisView.as_view())
]