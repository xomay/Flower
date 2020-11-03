from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.GroupeView.as_view()),
    path('<int:pk>/', views.GroupeDetailView.as_view())
]