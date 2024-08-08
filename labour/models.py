from django.db import models

# Create your models here.


class LabourType(models.Model):
    title = models.CharField(max_length=50)
    issue_date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.title


class LabourDeal(models.Model):
    PAYMENT_CHOICES = [
        ('Monthly', 'Monthly'),
        ('production', 'production'),
        ('Daily', 'Daily'),
    ]

    labour_type = models.ForeignKey(LabourType, on_delete=models.CASCADE)
    sarder_name = models.CharField(max_length=100)
    payment_sequence = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    requirements = models.TextField()
    issue_date = models.DateTimeField(auto_now=True)  
    number_of_employee = models.IntegerField()
    starting_date = models.DateField()
    closing_date = models.DateField()
    season_target = models.IntegerField(default=0)
    complete_production =  models.IntegerField(default=0)
    is_active = models.BooleanField(default = True)


    def __str__(self):
        return f"{self.labour_type} - {self.sarder_name}"


        

class LabourBill(models.Model):
    labour_deal = models.ForeignKey(LabourDeal, on_delete=models.CASCADE)
    bill_amount = models.DecimalField(max_digits=10, decimal_places=2)  
    date = models.DateTimeField(auto_now=False, auto_now_add = True, null=True)

    def __str__(self):
        return f"{self.labour_deal.sarder_name} - {self.date}"
    
