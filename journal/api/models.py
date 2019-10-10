from django.db import models
from uuid import uuid4

# Create your models here.
class Journal(models.Model):
    uuid = models.UUIDField(primary_key = True, default = uuid4, editable = False)
    name = models.CharField(max_length = 128, unique = True)

    foundation = models.DateField()
    publisher = models.UUIDField()

    class Meta:
        ordering = ('address', )

    def __str__(self) -> str:
        return self.name
