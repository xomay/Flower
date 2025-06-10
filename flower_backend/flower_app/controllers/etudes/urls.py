from django.urls import include, path
from . import views

#Base url for here is '/etudes/'

urlpatterns = [
    path('', views.EtudeListCreateView.as_view()),
    path('cc/', views.CCListCreateView.as_view()),
    path('<int:pk>/', views.EtudeRetrieveUpdateView.as_view()),
    path('<int:id>/files/', views.EtudeEditFiles.as_view()),
    path('<int:pk>/ce/', views.CEView.as_view()),
    path('<int:pk>/cc/', views.CCView.as_view()),
    path('<int:pk>/missions/', views.MissionsView.as_view()),
    path('<int:project_id>/bvs/', views.BVsView.as_view()),
    path('<int:project_id>/missions/<int:pk>/', views.MissionsDetailView.as_view()),
    path('getReaEtudes/', views.ReaEtudesView.as_view()),
    path('getReaEtudes/<int:etude_id>/', views.ReaEtudesDetailView.as_view())
]