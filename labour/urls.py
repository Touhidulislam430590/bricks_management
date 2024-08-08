from django.urls import path
from . import views

urlpatterns = [
    path('', views.labours, name='labours'),
    path('new_deal/', views.new_deal, name='new_deal'),
    path('add_type/', views.add_type, name='add_type'),
    path('due_labour/', views.due_labour, name='due_labour'),
    path('due_labour_search/', views.due_labour_search, name='due_labour_search'),
    path('complete_bills/', views.complete_bills, name='complete_bills'),
    path('labour_bill_history/', views.labour_bill_history, name='labour_bill_history'),
    path('history_search/', views.history_search, name='history_search'),
    path('due_labour_details/<int:id>', views.due_labour_details, name='due_labour_details'),
    path('labour_bill_invoice/<int:id>', views.labour_bill_invoice, name='labour_bill_invoice'),
]
