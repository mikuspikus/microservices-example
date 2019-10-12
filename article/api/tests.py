from django.test import TestCase
from django.urls import reverse
import json

from rest_framework.test import APIClient, force_authenticate, APITestCase
from rest_framework.authtoken.models import Token

from .models import Article, Author

class ArticlesAPIViewTestCase(APITestCase):
    url = '/articles/'

    def test_create_article(self):
        article_data = {
            "title" : "First",
            "published" : "2019-12-03",
            "authors" : [
                { "author_uuid" : "00000000-0000-0000-0000-000000000001" }, 
                { "author_uuid" : "00000000-0000-0000-0000-000000000002" }, 
                { "author_uuid" : "00000000-0000-0000-0000-000000000003" }
            ],
            "publisher" : "00000000-0000-0000-0000-000000000001",
            "journal" : "00000000-0000-0000-0000-000000000001"
        }

        response = self.client.post(self.url, article_data, format = 'json')

        self.assertEqual(201, response.status_code)

    def test_no_authors(self):
        article_data = {
            "title" : "Second",
            "published" : "2019-12-03",
            "publisher" : "00000000-0000-0000-0000-000000000001",
            "journal" : "00000000-0000-0000-0000-000000000001"
        }

        response = self.client.post(self.url, article_data, format = 'json')

        self.assertEqual(400, response.status_code)

    def test_unique_article_names(self):
        article_data_fst = {
            "title" : "Third",
            "published" : "2019-12-03",
            "authors" : [
                { "author_uuid" : "00000000-0000-0000-0000-000000000001" }, 
                { "author_uuid" : "00000000-0000-0000-0000-000000000002" }, 
                { "author_uuid" : "00000000-0000-0000-0000-000000000003" },
            ],
            "publisher" : "00000000-0000-0000-0000-000000000001",
            "journal" : "00000000-0000-0000-0000-000000000001"
        }

        response = self.client.post(self.url, article_data_fst, format = 'json')

        self.assertEqual(201, response.status_code)

        article_data_snd = {
            "title" : "Third",
            "published" : "2019-12-03",
            "authors" : [
                { "author_uuid" : "00000000-0000-0000-0000-000000000001" }, 
                { "author_uuid" : "00000000-0000-0000-0000-000000000002" }, 
                { "author_uuid" : "00000000-0000-0000-0000-000000000003" },
            ],
            "publisher" : "00000000-0000-0000-0000-000000000001",
            "journal" : "00000000-0000-0000-0000-000000000001"
        }

        response = self.client.post(self.url, article_data_snd, format = 'json')

        self.assertEqual(400, response.status_code)

    def test_get_valid_filter(self):
        filter_ = '?publisher=00000000-0000-0000-0000-000000000001'

        response = self.client.get(self.url + filter_)

        self.assertEqual(200, response.status_code)

    def test_get_invalid_filter(self):
        filter_ = '?memes=Pupa'

        response = self.client.get(self.url + filter_)

        self.assertEqual(400, response.status_code)

    def test_get_all(self):
        response = self.client.get(self.url)

        self.assertEqual(200, response.status_code)

class ArticleAPIViewTestCase(APITestCase):
    url = '/articles/'

    def setUp(self):
        self.title = "The world-wide appreciation of 'Pupa and Lupa' jokes"
        self.published = "2019-12-03"
        self.authors = [
                { "author_uuid" : "00000000-0000-0000-0000-000000000001" }, 
                { "author_uuid" : "00000000-0000-0000-0000-000000000002" }, 
                { "author_uuid" : "00000000-0000-0000-0000-000000000003" },
        ]
        self.publisher = 1
        self.journal = 1
        self.article, created = Article.objects.get_or_create(
            title = self.title,
            published = self.published,
            publisher =self.publisher,
            journal = self.journal,
        )

    def test_invalid_uuid(self):
        uuid_ = "00000000-0000-0000-0000-000000000001"
        response = self.client.get(self.url + f'{uuid_}/')

        self.assertEqual(404, response.status_code)

    def test_valid_uuid(self):
        uuid_ = self.article.uuid
        response = self.client.get(self.url + f'{uuid_}/')

        self.assertEqual(200, response.status_code)

    def test_patch_article(self):
        self.article, created = Article.objects.get_or_create(
            title = self.title,
            published = self.published,
            publisher =self.publisher,
            journal = self.journal,
        )

        uuid_ = self.article.uuid
        article_data = {
            "title" : self.title,
            "published" : "2039-12-03",
            "authors" : self.authors,
            "publisher" : self.publisher,
            "journal" : self.journal
        }

        response = self.client.patch(self.url + f'{uuid_}/', data = article_data, format = 'json')

        self.assertEqual(202, response.status_code)

    def test_delete_article(self):
        uuid_ = self.article.uuid
        response = self.client.delete(self.url + f'{uuid_}/')

        self.assertEqual(204, response.status_code)