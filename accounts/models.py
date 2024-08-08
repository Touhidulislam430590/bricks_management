from django.db import models

# Create your models here.


class Miscellaneous(models.Model):
    title = models.CharField(max_length=100)
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now=False, auto_now_add = True)

    def __str__(self):
        return f"{self.title} - {self.date}"