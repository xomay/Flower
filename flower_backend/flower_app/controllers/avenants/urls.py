from django.urls import include, path
from . import views

#Base url for here is '/avenants/'

urlpatterns = [
    path('', views.AvenantListCreateView.as_view()),
    path('<int:pk>/', views.AvenantRetrieveUpdateDestroyView.as_view()),
]
