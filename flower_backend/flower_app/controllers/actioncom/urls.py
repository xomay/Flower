from django.urls import include, path
from . import views

#Base url for here is '/actioncom/'

urlpatterns = [
    path('types', views.ActionsTypesView.as_view()),
    path('', views.ActionsCommercialesListCreateView.as_view()),
    path('<int:id>/', views.ActionsCommercialesDetailView.as_view()),
]
