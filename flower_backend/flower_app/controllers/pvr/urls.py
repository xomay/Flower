from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.PVRListCreateView.as_view()),
    path('<int:pk>/', views.PVRRetrieveUpdateDestroyView.as_view()),
]
