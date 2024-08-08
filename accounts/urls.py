from django.urls import path
from . import views

urlpatterns = [
    path('', views.accounts, name='accounts'),
    path('search_accounts/', views.search_accounts, name='search_accounts'),
    path('miscelleneous/', views.miscelleneous, name='miscelleneous'),
    path('search_miscllenous/', views.search_miscllenous, name='search_miscllenous')
]
