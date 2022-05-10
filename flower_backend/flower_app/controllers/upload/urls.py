from django.urls import include, path
from . import views

#Base url for here is '/upload/'

urlpatterns = [
    path('', views.UploadsView.as_view()),
    path('memory/', views.GetMemoryView.as_view()),
    path('<int:id>/', views.UploadFileView.as_view()),
    path('<int:id>/shared/<str:key>', views.SharedUploadFileView.as_view()),
    path('sharedurl/<int:id>/', views.GetSharedUploadFilePath.as_view())
]