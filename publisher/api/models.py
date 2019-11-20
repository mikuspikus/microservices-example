from django.db import models

from uuid import uuid4

class Publisher(models.Model):
    uuid = models.UUIDField(primary_key = True, editable = False, default = uuid4)
    name = models.CharField(max_length = 128, unique = True)

    editor = models.CharField(max_length = 128)
    address = models.CharField(max_length = 128)

class Journal(models.Model):
    uuid = models.UUIDField()
    publisher = models.ForeignKey(Publisher, related_name = "journals", on_delete = models.CASCADE)

