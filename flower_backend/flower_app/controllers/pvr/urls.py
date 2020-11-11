from django.urls import include, path
from . import views

#Base url for here is '/pvr/'

urlpatterns = [
    path('', views.PVRListCreateView.as_view()),
    path('<int:pk>/', views.PVRRetrieveUpdateDestroyView.as_view()),
]
