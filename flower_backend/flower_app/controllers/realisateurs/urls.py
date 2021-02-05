from django.urls import include, path
from . import views

#Base url for here is '/realisateurs/'

urlpatterns = [
    # Réalisateurs
    path('', views.RealisateurListCreateView.as_view()),
    path('<int:id>/', views.RealisateurRetrieveUpdateDestroyView.as_view()),
    # Commentaires
    path('cmts/', views.CommentsListCreateView.as_view()),
    path('cmts/<int:id>/', views.CommentsRetrieveUpdateDestroyView.as_view()),
    # Skills
    path('skills/', views.SkillsRetrieveUpdateDestroyView.as_view())
]