from django.test import TestCase
from django.urls import reverse
import json

from rest_framework.test import APIClient, force_authenticate, APITestCase
from rest_framework.authtoken.models import Token

from .models import Publisher, Journal, CustomToken

class PublishersAPIViewTestCase(APITestCase):
    url = '/publishers/'
    token = ''
    keyword = 'Bearer'

    def setUp(self):
        token = CustomToken.objects.create()
        self.client.credentials(HTTP_AUTHORIZATION = f'{self.keyword} {token.token}')

    def test_create_publisher(self):
        p_data = {
            'name' : 'Pupa\'s Publishing Co.',
            'editor' : 'Pupa',
            'address' : 'Pupa\'s house',
            'journals' : [
                {'uuid' : 1},
                {'uuid' : 2}
            ]
        }

        response = self.client.post(self.url, p_data, format = 'json')

        self.assertEqual(201, response.status_code)

    def test_no_journals(self):
        p_data_fst = {
            'name' : 'Lupa\'s Publishing Co.',
            'editor' : 'Lupa',
            'address' : 'Lupa\'s house',
        }

        response = self.client.post(self.url, p_data_fst)

        self.assertEqual(400, response.status_code)

    def test_get_valid_filter(self):
        filter_ = '?editor=Pupa'

        response = self.client.get(self.url + filter_)

        self.assertEqual(200, response.status_code)

    def test_get_invalid_filter(self):
        filter_ = '?memes=Pupa'

        response = self.client.get(self.url + filter_)

        self.assertEqual(400, response.status_code)

    def test_get_all(self):
        response = self.client.get(self.url)

        self.assertEqual(200, response.status_code)

class PublisherAPIViewTestCase(APITestCase):
    url = '/publishers/'
    token = ''
    keyword = 'Bearer'

    def setUp(self):
        token = CustomToken.objects.create()
        self.client.credentials(HTTP_AUTHORIZATION = f'{self.keyword} {token.token}')
        self.name = "Funky Publisher"
        self.editor = "Don Digidon"
        self.journals = [
                { "uuid" : "00000000-0000-0000-0000-000000000001" }, 
                { "uuid" : "00000000-0000-0000-0000-000000000002" }, 
                { "uuid" : "00000000-0000-0000-0000-000000000003" },
        ]
        self.address = "Your mom's house"

        self.publisher, created = Publisher.objects.get_or_create(
            name = self.name,
            editor = self.editor,
            address =self.address
        )

    def test_invalid_uuid(self):
        uuid_ = "00000000-0000-0000-0000-000000000001"
        response = self.client.get(self.url + f'{uuid_}/')

        self.assertEqual(404, response.status_code)

    def test_valid_uuid(self):
        uuid_ = self.publisher.uuid
        response = self.client.get(self.url + f'{uuid_}/')

        self.assertEqual(200, response.status_code)

    def test_patch_publisher(self):
        self.publisher, created = Publisher.objects.get_or_create(
            name = self.name,
            editor = self.editor,
            address =self.address
        )

        uuid_ = self.publisher.uuid

        publisher_data = {
            "name" : self.name,
            "editor" : self.editor,
            "address" : self.address,
            "journals" : self.journals
        }

        response = self.client.patch(self.url + f'{uuid_}/', data = publisher_data, format = 'json')

        self.assertEqual(202, response.status_code)

    def test_delete_publisher(self):
        uuid_ = self.publisher.uuid
        response = self.client.delete(self.url + f'{uuid_}/')

        self.assertEqual(204, response.status_code)
