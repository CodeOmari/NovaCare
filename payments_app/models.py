from django.db import models
from user_management.models import Details


# Create your models here.
class Payment(models.Model):
    details = models.ForeignKey(Details, on_delete=models.CASCADE)
    merchant_request_id = models.CharField(max_length=100)
    checkout_request_id = models.CharField(max_length=100)
    code = models.CharField(max_length=30, null=True)
    status = models.CharField(max_length=20, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return f"{self.details}-{self.code} - {self.status}"

    class Meta:
        db_table = 'payments'

    
class Amount(models.Model):
    fee = models.IntegerField()

    def __str__(self):
        return self.fee
    

    class Meta:
        db_table = 'amount'