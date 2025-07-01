from django.urls import include, path
from . import views

#Base url for here is '/etudes/phases/'

urlpatterns = [
    path('', views.PhaseEtudeView.as_view()),
    path('<int:pk>/', views.PhaseEtudeDetailView.as_view()),
    path('missions/', views.PhaseMissionView.as_view()),
    path('missions/<int:pk>/', views.PhaseMissionDetailView.as_view())
]