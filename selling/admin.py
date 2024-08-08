from django.contrib import admin
from .models import Selling, Selling_payment_history

# Register your models here.

admin.site.register(Selling)
admin.site.register(Selling_payment_history)