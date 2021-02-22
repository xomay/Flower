from django.urls import include, path
from . import views

#Base url for here is '/ndfs/details/'

urlpatterns = [
    path('', views.NdFDetailView.as_view()),
    path('<int:pk>/', views.NdFDetailDetailView.as_view())
]