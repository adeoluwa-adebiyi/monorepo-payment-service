from django.db import models
from polymorphic.models import PolymorphicModel

# Create your models here.

TRANSACTION_STATES = [
    ("PENDING", "PENDING"),
    ("FAILED", "FAILED"),
    ("SUCCESS", "SUCCESS")
]

class Transaction(PolymorphicModel):

    id = models.AutoField(primary_key=True)
    status = models.CharField(choices=TRANSACTION_STATES, default="PENDING", max_length=10)
    amount = models.DecimalField(max_digits=20, decimal_places=8, null=False)
    charge_response = models.JSONField(null=True)
    validate_response = models.JSONField(null=True)


class OrderTransaction(Transaction):

    trxjob_id = models.IntegerField(unique=True)

