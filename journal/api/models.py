from django.db import models
from uuid import uuid4

import binascii, os

# Create your models here.
class Journal(models.Model):
    uuid = models.UUIDField(primary_key = True, default = uuid4, editable = False)
    name = models.CharField(max_length = 128, unique = True)

    foundation = models.DateField()
    publisher = models.UUIDField(null = True)

    def __str__(self) -> str:
        return self.name

class CustomToken(models.Model):
    token = models.CharField(verbose_name = 'Token', max_length = 40)
    created = models.DateTimeField(verbose_name = 'Creation Date', auto_now_add = True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_token()

        return super().save(*args, **kwargs)

    def generate_token(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.token