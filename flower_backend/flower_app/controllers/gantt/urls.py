from django.urls import include, path
# from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('etude/<int:etude_id>/', views.GanttView.as_view()),
]
# urlpatterns = format_suffix_patterns(urlpatterns, allowed=['format'])