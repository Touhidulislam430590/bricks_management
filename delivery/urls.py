from django.urls import path
from . import views

urlpatterns = [
    path('', views.delivery, name='delivery'),
    path('ready/<int:id>', views.ready_to_delivery, name='ready'),
    path('delivery_details/<int:id>', views.delivery_info, name='delivery_details'),
    path('delivery_done/', views.delivery_done, name='delivery_done'),
    path('delivery_report/', views.delivery_report, name='delivery_report'),
    path('delivery_challan/<int:id>', views.delivery_challan, name='delivery_challan'),
    path('search_delivery/', views.search_delivery_history, name='search_delivery'),
    path('delivery_search/', views.delivery_search, name='delivery_search'),
    path('delivery_done_search/', views.delivery_done_search, name='delivery_done_search'),
]
