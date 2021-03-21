from django.urls import include, path
from . import views

#Base url for here is '/signature/'

urlpatterns = [
    path('', views.GenerateSignature.as_view())
]