from django.db import models
from home.models import Base

# Create your models here.


class Selling(models.Model):
    sell_type = (
        ('Instant Selling', 'Instant Selling'),
        ('Advance Selling', 'Advance Selling'),
    )


    brick = (
        ('Number 1', 'Number 1'),
        ('Number 2', 'Number 2'),
        ('Number 3', 'Number 3'),
        ('picked', 'picked'),
        ('Half Bricks', 'Half Bricks')
    )

    selling_type = models.CharField(choices = sell_type, max_length=50)
    Bricks_type = models.CharField(choices = brick, max_length=50)
    customer_name = models.CharField(max_length=50)
    customer_address = models.CharField(max_length=200)
    customer_mobile = models.IntegerField()
    product_rate = models.IntegerField()
    product_quantity = models.IntegerField()
    total_price = models.FloatField()
    payment = models.FloatField()
    commission = models.IntegerField(default = 0)
    due = models.FloatField(default = 0)
    is_pending = models.BooleanField(default = False)
    is_delivered = models.BooleanField(default = False)
    issue_date = models.DateTimeField(auto_now = True, null = True)

    def __str__(self):
        return self.customer_name
    

class Selling_payment_history(models.Model):
    customer_name = models.CharField(max_length=50)
    amount = models.FloatField()
    issue_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer_name} - {self.amount}"