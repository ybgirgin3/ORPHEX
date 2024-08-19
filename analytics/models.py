from django.db import models

# Create your models here.

from django.db import models

class Data(models.Model):
    customer_id = models.CharField(max_length=100)
    revenue = models.FloatField()
    conversions = models.IntegerField()
    status = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    category = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self): # type: ignore
        return self.customer_id

