from django.db import models

class Bank(models.Model):
    code = models.CharField(max_length=10, unique=True)  
    name = models.CharField(max_length=100)
    swift_code = models.CharField(max_length=11, unique=True)
    country = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} ({self.code})"

class Branch(models.Model):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    branch_code = models.CharField(max_length=10)
    address = models.TextField()
    phone = models.CharField(max_length=15)

    class Meta:
        unique_together = ('bank', 'branch_code')
