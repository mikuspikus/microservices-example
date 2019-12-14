from django.db import models

from uuid import uuid4
import binascii, os

class Publisher(models.Model):
    uuid = models.UUIDField(primary_key = True, editable = False, default = uuid4)
    name = models.CharField(max_length = 128, unique = True)

    editor = models.CharField(max_length = 128)
    address = models.CharField(max_length = 128)

class Journal(models.Model):
    uuid = models.UUIDField()
    publisher = models.ForeignKey(Publisher, related_name = "journals", on_delete = models.CASCADE, null = True)

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