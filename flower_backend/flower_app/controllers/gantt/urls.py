from django.urls import include, path
from . import views

#Base url for here is '/gantt/'

urlpatterns = [
    path('etude/<int:etude_id>/', views.GanttView.as_view())
]