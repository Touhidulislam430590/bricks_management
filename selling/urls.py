from django.urls import path
from . import views

urlpatterns = [
    path('', views.selling, name='selling'),
    path('sell/<int:id>', views.sellInfo, name='sell'),
    path('due/', views.due_payment, name='due_list'),
    path('sell_print/<int:id>', views.sell_print, name='sell_print'),
    path('due/<int:id>', views.due_form, name='due_info'),
    path('due_invoice/<int:id>', views.due_invoice, name='due_invoice'),
    path('search_selling/', views.search_selling, name='search_selling'),
    path('due_search_selling/', views.due_search_selling, name='due_search_selling'),
    path('payment_history/', views.payment_history, name='payment_history'),
    # path('due/<int:id>', views.due_payment, name='due_list'),
]