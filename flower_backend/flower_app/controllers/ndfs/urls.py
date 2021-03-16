from django.urls import include, path
from . import views

#Base url for here is '/ndfs/'

urlpatterns = [
    path('', views.NFListView.as_view()),
    path('<int:pk>/', views.NFRetrieveUpdateDestroyView.as_view()),
    path('<int:id>/files/', views.NFEditFiles.as_view()),
]