from django.db import models
from django.contrib.auth.models import AbstractUser

import uuid

class GatewayUser(AbstractUser):
    outer_uuid = models.UUIDField(unique = True, default = uuid.uuid4, editable = False)
    token = models.CharField(max_length=128)
    identifier = models.IntegerField()