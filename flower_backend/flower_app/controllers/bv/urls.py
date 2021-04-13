from django.urls import include, path
from . import views

#Base url for here is '/bv/'

urlpatterns = [
    path('', views.BVView.as_view()),
    path('<int:pk>/', views.BVDetailView.as_view())
]