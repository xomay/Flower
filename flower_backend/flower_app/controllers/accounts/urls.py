from django.urls import include, path
from . import views

#Base url for here is '/accounts/'

urlpatterns = [
    path('login', views.LoginView.as_view()),
    path('logout', views.LogoutView.as_view()),
]