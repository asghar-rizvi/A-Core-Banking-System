from django.db import models
from Accounts.models import Account

class Transaction(models.Model):
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='sent_transactions')
    receiver = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='received_transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
        ('PENDING', 'Pending')
    ], default='PENDING')
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.sender.account_number} → {self.receiver.account_number} | Rs.{self.amount}"
