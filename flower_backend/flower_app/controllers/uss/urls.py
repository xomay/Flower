from django.urls import include, path
from . import views

#Base url for here is '/etudes/uss/'

urlpatterns = [
    path('', views.USView.as_view()),
    path('<int:pk>/', views.USDetailView.as_view())
]