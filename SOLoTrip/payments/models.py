from django.db import models
from trips.models import Trip

# Create your models here.
class Payment(models.Model):
    amount = models.IntegerField()
    pay_date = models.DateField(auto_now=False, auto_now_add=False)
    pay_time = models.TimeField(auto_now=False, auto_now_add=False)
    mutual = models.CharField(max_length=30)  # 상호명
    category = models.CharField(max_length=10, default="")
    bank_account = models.CharField(max_length=30)
    transaction_type = models.CharField(max_length=15)
    transaction_unique_number = models.IntegerField()