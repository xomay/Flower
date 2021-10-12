from django.urls import include, path
from . import views

#Base url for here is '/doctypes/'

urlpatterns = [
    path('', views.PhaseView.as_view()),
    path('<int:pk>/', views.PhaseDetailView.as_view())
]