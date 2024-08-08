from django.urls import path
from . import views

urlpatterns = [
    path('', views.production, name='production'),
    path('search_production/', views.search_production, name='search_production')
]
