from django.urls import include, path
from . import views
from django.views.decorators.csrf import csrf_exempt
#Base url for here is '/membres/'

urlpatterns = [
    path('', views.MembreView.as_view()),
    path('<int:pk>/', views.MembreDetailView.as_view()),
    path('openaccount/<int:pk>/', csrf_exempt(views.OpenAccountView.as_view())),
    
]