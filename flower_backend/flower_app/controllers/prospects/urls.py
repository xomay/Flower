from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.ProspectListCreateView.as_view()),
    path('<int:pk>/', views.ProspectRetrieveUpdateDestroyView.as_view()),
    path('<int:id>/employes/', views.EmployeListCreateView.as_view()),
    path('<int:prospect_id>/employes/<int:id>/', views.EmployeRetrieveUpdateDestroyView.as_view())
]