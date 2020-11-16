from django.urls import include, path
from . import views

#Base url for here is '/tresorerie/facture/'

urlpatterns = [
    path('', views.FactureView.as_view()),
    path('<int:pk>/', views.FactureLineView.as_view()),
    path('detail/<int:pk>/', views.RemoveFactureLineView.as_view())
]
