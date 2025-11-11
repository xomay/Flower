from django.urls import include, path
from . import views

# Base url for here is '/requirements/'
urlpatterns = [
    path('', views.RequirementListCreateUpdateView.as_view()),
    path('<int:pk>/', views.RequirementDestroyView.as_view()),
]