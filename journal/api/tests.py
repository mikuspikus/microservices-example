from django.test import TestCase
from django.urls import reverse
import json

from rest_framework.test import APIClient, force_authenticate, APITestCase
from rest_framework.authtoken.models import Token

from .models import Journal

class JournalsAPIViewTestCase(APITestCase):
    url = '/journals/'

    def test_create_journal(self):
        j_data = {
            "name" : "Pupa's Journal",
            "foundation" : "2019-12-03",
            "publisher" : 1
        }

        response = self.client.post(self.url, j_data, format = 'json')

        self.assertEqual(201, response.status_code)

    def test_unique_journal_name(self):
        j_data_fst = {
            "name" : "Lupa's Journal",
            "foundation" : "2019-12-03",
            "publisher" : 1
        }
        response = self.client.post(self.url, j_data_fst, format = 'json')
        self.assertEqual(201, response.status_code)

        j_data_snd = {
            "name" : "Lupa's Journal",
            "foundation" : "2019-12-03",
            "publisher" : 1
        }
        response = self.client.post(self.url, j_data_snd, format = 'json')
        self.assertEqual(400, response.status_code)

    def test_get_all(self):
        response = self.client.get(self.url)

        self.assertEqual(200, response.status_code)

class JournalAPIViewTestCase(APITestCase):
    url = '/journals/'

    def setUp(self):
        self.name = "Lupa's Journal"
        self.foundation = "2019-12-03"
        self.publisher = 1

        self.journal, created = Journal.objects.get_or_create(
            name = self.name,
            foundation = self.foundation,
            publisher = self.publisher
        )

    def test_invalid_uuid(self):
        uuid_ = "00000000-0000-0000-0000-000000000001"
        response = self.client.get(self.url + f'{uuid_}/')

        self.assertEqual(404, response.status_code)

    def test_valid_uuid(self):
        uuid_ = self.journal.uuid
        response = self.client.get(self.url + f'{uuid_}/')

        self.assertEqual(200, response.status_code)

    def test_patch_journal(self):
        self.journal, created = Journal.objects.get_or_create(
            name = self.name,
            foundation = self.foundation,
            publisher = self.publisher,
        )

        uuid_ = self.journal.uuid
        journal_data = {
            "name" : self.name,
            "foundation" : "2039-12-03",
            "publisher" : self.publisher,
        }

        response = self.client.patch(self.url + f'{uuid_}/', data = journal_data, format = 'json')

        self.assertEqual(202, response.status_code)

    def test_delete_journal(self):
        uuid_ = self.journal.uuid
        response = self.client.delete(self.url + f'{uuid_}/')

        self.assertEqual(204, response.status_code)
