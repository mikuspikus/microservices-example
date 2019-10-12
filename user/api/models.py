from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid

# created my models here
'''
class CustomUserManager(BaseUserManager):
    use_in_migration = True

    def create_user(self, username: str, password: str):
        user = self.model(
            username = username
        )

        user.set_password(password)
        user.save(using = self._db)

        return user

    def create_staffuser(self, username: str, password: str):
        user = self.create_user(
            username = username,
            password = password
        )

        user.staff = True

        user.save(using=self._db)

        return user

    def create_superuser(self, username: str,  password: str):
        user = self.create_user(
            username = username,
            password = password
        )
        user.staff = True
        user.admin = True
        
        user.save(using=self._db)

        return user
'''

class CustomUser(AbstractUser):
    outer_uuid = models.UUIDField(unique = True, default = uuid.uuid4, editable = False)

    #objects = CustomUserManager()
