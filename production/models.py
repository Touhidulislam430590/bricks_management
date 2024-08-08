from django.db import models
from labour.models import LabourDeal

# Create your models here.

class Daily_Production(models.Model):
    labour_instance = models.ForeignKey(LabourDeal, on_delete=models.CASCADE)
    production = models.IntegerField()
    description = models.TextField(max_length=200)
    total_bill = models.IntegerField()
    paid_bill = models.IntegerField()
    due_bill = models.IntegerField(default=0)
    issue_date = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.labour_instance.labour_type} - {self.labour_instance.sarder_name} - {self.production}"
    