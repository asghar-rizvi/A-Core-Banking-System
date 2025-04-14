from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(max_length=15)
    kyc_verified = models.BooleanField(default=False)
    
    @property
    def token_payload(self):
        return {
            'user_id': self.id,
            'email': self.email,
            'phone': self.phone
        }

    