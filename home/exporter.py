# myapp/exporters.py
import csv
from django.http import HttpResponse

def export_models_to_csv(models, response):
    writer = csv.writer(response)
    
    for model in models:
        fields = [field.name for field in model._meta.fields]
        writer.writerow([model._meta.verbose_name])
        writer.writerow(fields)
        
        for obj in model.objects.all():
            row = [getattr(obj, field) for field in fields]
            writer.writerow(row)
        
        writer.writerow([])