from django.urls import include, path
from . import views

#Base url for here is '/etudes/uss/'

urlpatterns = [
    path('', views.USView.as_view()),
    path('<int:pk>/', views.USDetailView.as_view()),
    path('rea/<int:uss_id>/<new_state>/', views.ReaUpdateUSView.as_view())
]