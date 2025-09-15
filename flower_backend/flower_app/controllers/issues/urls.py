from django.urls import include, path
from . import views

#Base url for here is '/issues/'

urlpatterns = [
    path('', views.IssueCreateView.as_view()),
]