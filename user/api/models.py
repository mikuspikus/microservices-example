from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# created my models here
class CustomUser(AbstractUser):
    outer_uuid = models.UUIDField(unique = True, default = uuid.uuid4, editable = False)
