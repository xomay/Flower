from django.urls import include, path
from . import views

#Base url for here is '/administration/'

urlpatterns = [
    # Paramètres généraux
    path('params', views.GetParametersJE.as_view()),
    path('params/<requ>/', views.GetParameter.as_view()),

    # Postes
    path('postes/', views.PostesCreateView.as_view()),
    path('postes/<int:pk>/', views.PostesUpdateDestroyView.as_view()),
]