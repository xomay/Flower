from django.urls import include, path
from . import views

#Base url for here is '/administration/'

urlpatterns = [
    path('params', views.GetParametersJE.as_view()),
    path('params/<requ>/', views.GetParameter.as_view())
]