from django.urls import include, path
from . import views

#Base url for here is '/membres/'

urlpatterns = [
    path('', views.MembreView.as_view()),
    path('<int:pk>/', views.MembreDetailView.as_view()),
    path('openaccount/<int:pk>/', views.OpenAccountView.as_view()),
]