from django.urls import include, path
from . import views

#Base url for here is '/tresorerie/factures/'

urlpatterns = [
    path('', views.FactureView.as_view()),
    path('count/', views.GetMonthAmount.as_view()),
    path('count/<dateSelector>/', views.GetMonthAmountSel.as_view()),
    path('<int:pk>/', views.FactureLineView.as_view()),
    path('detail/<int:pk>/', views.RemoveFactureLineView.as_view())
]
