from django.urls import include, path
from . import views

#Base url for here is '/membres/'

urlpatterns = [
    path('', views.MembreView.as_view()),
    path('<int:id>/', views.MembreDetailView.as_view())
]