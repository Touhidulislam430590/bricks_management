from django.contrib import admin
from .models import Soil, Petroleum, Material_payment_history

# Register your models here.

admin.site.register(Petroleum)
admin.site.register(Soil)
admin.site.register(Material_payment_history)