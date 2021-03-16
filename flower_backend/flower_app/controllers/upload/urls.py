from django.urls import include, path
from . import views

#Base url for here is '/upload/'

urlpatterns = [
    path('', views.UploadsView.as_view()),
    path('memory/', views.GetMemoryView.as_view()),
    path('<int:id>/', views.UploadFileView.as_view())
]