import uuid
from django.db import models

# Create your models here.

class Company(models.Model):
    cname = models.TextField(max_length=20)
    cmobile = models.TextField(max_length=14)
    caddress = models.TextField(max_length=100)

    def __str__(self):
        return self.cname
    


class Base(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        abstract = True