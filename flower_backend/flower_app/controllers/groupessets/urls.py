from django.urls import include, path
from . import views

#Base url for here is '/etudes/grouessets/'

urlpatterns = [
    path('', views.GSListCreateView.as_view()),
    path('<int:pk>/', views.GSRetrieveUpdateDestroyView.as_view()),
]
