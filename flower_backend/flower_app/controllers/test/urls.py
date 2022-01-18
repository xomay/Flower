from django.urls import include, path
from . import views

#Base url for here is '/test/'

urlpatterns = [
    path('', views.TestView.as_view()),
]
