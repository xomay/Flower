from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.MembreView.as_view()),
    path('<int:id>/', views.MembreDetailView.as_view())
]