from django.contrib import admin
from .models import LabourType, LabourDeal, LabourBill

# Register your models here.

admin.site.register(LabourType)
admin.site.register(LabourDeal)
admin.site.register(LabourBill)
