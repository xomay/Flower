from django.urls import include, path
from . import views

#Base url for here is '/contactway/'

urlpatterns = [
    path('', views.ContactWayListCreateView.as_view()),
    path('<int:id>/', views.ContactWayRetrieveUpdateDestroyView.as_view())
]