from django.urls import include, path
from . import views

#Base url for here is '/etudes/'

urlpatterns = [
    path('', views.EtudeListCreateView.as_view()),
    path('<int:pk>/', views.EtudeRetrieveUpdateView.as_view()),
    path('<int:pk>/ce/', views.CEView.as_view()),
    path('<int:pk>/missions/', views.MissionsView.as_view()),
    path('<int:project_id>/missions/<int:pk>/', views.MissionsDetailView.as_view())
]