from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.AvenantEtudeView.as_view()),
    path('<int:pk>/', views.AvenantEtudeDetailView.as_view()),
    path('missions/', views.AvenantMissionView.as_view()),
    path('missions/<int:pk>/', views.AvenantMissionDetailView.as_view()),
]