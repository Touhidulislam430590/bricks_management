from django.db import models

# Create your models here.

class Petroleum(models.Model):
    PETROLEUM_CHOICE = [
        ('Coal', 'Coal'),
        ('Wood', 'Wood'),
    ]

    petroleum_type = models.CharField(max_length=10, choices = PETROLEUM_CHOICE)
    vendor_name = models.CharField(max_length=50)
    quantity = models.FloatField()
    rate = models.FloatField()
    total_price = models.FloatField()
    done_payment = models.FloatField()
    due = models.FloatField()
    issue_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.vendor_name} - {self.petroleum_type}"
    

class Soil(models.Model):
    vendor_name = models.CharField(max_length=50)
    quantity = models.FloatField()
    rate = models.FloatField()
    total_price = models.FloatField()
    sarder_name = models.CharField(max_length=50)
    done_payment = models.FloatField()
    due = models.FloatField()
    issue_date = models.DateTimeField(auto_now_add=True, null=True) 

    def __str__(self):
        return f"{self.vendor_name} - {self.sarder_name}"


class Material_payment_history(models.Model):
    vendor_name = models.CharField(max_length=50)
    amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vendor_name} - {self.amount}"