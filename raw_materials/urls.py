from django.urls import path
from . import views

urlpatterns = [
    path('', views.raw_materials, name="raw_materials"),
    path('search_raw_materials/', views.search_raw_materials, name="search_raw_materials"),
    path('soil/', views.soil, name='soil'),
    path('petroleum/', views.petroleum, name='petroleum'),
    path('due_materials/', views.due_materials, name='due_materials'),
    path('material_payment_history/', views.material_payment_history, name='material_payment_history'),
    path('due_details/<int:id>/<str:vendor_name>', views.due_details, name='due_details'),
    path('due_invoice/<int:id>/<str:data_type>', views.due_invoice, name='due_invoice'),
]
