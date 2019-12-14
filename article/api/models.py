from django.db import models
import uuid as uuid_

import binascii, os

# Create your models here.
class Author(models.Model):

    # author_uuid recreates with default = True
    # add id?
    # delete default?
    author_uuid = models.UUIDField()
    # user-api-user

    class Meta:
        verbose_name = ("Author")
        verbose_name_plural = ("Authors")
        ordering = ('author_uuid', )

    def __str__(self) -> str:
        return str(self.author_uuid)


class Article(models.Model):
    uuid = models.UUIDField(primary_key = True, default = uuid_.uuid4)
    title = models.CharField(max_length = 128, unique = True)
    added = models.DateField(auto_now_add = True)
    published = models.DateField()

    authors = models.ManyToManyField(Author)
    journal = models.UUIDField()
    # models.ForeignKey(journal-api-journal, on_delete=models.CASCADE)

    class Meta:
        ordering = ('title', 'added', )
        verbose_name = ("Article")
        verbose_name_plural = ("Articles")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Article_detail", kwargs={"pk": self.pk})

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