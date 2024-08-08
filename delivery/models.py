from django.db import models

# Create your models here.

class Delivery(models.Model):
    selling_id = models.IntegerField()
    customer_name = models.CharField(max_length=50)
    customer_address = models.CharField(max_length=200)
    customer_mobile = models.IntegerField()
    product_quantity = models.IntegerField()
    pending_delivery = models.IntegerField(default = 0)
    delivered = models.IntegerField(default = 0)

    def __str__(self):
        return self.customer_name
    

class Delivery_History(models.Model):
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE)
    delivery_amount = models.IntegerField()
    driver_name = models.TextField(max_length = 100, blank = True, default = 'None')
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.delivery.customer_name} - {self.created}"