from django.db import models
from django.conf import settings


class Trip(models.Model):
    country = models.CharField(max_length=30, null=False, blank=False)
    city = models.CharField(max_length=30, null=False, blank=False)
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField()
    budget = models.IntegerField()
    
    
class Member(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    budget = models.IntegerField(default=0)
    bank_account = models.CharField(max_length=30, default="")
    is_participate = models.BooleanField(default=True)