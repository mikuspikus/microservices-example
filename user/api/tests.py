import json

from rest_framework.test import APIClient, force_authenticate, APITestCase
from rest_framework.authtoken.models import Token

from django.urls import reverse

from .models import CustomUser

class UserRegistrationAPIViewTestCase(APITestCase):
    url = '/user/register/'

    def test_user_registration(self):
        user_data = {
            "username": "testuser",
            "password": "123123",
            "confirm_password": "123123"
        }

        response = self.client.post(self.url, user_data, format = 'json')

        self.assertEqual(201, response.status_code)

    def test_unique_username_validation(self):
        user_data_1 = {
            "username": "testuser",
            "password": "123123",
            "confirm_password": "123123"
        }

        response = self.client.post(self.url, user_data_1, format = 'json')

        self.assertEqual(201, response.status_code)

        user_data_2 = {
            "username": "testuser",
            "password": "123123",
            "confirm_password": "123123"
        }

        response = self.client.post(self.url, user_data_2, format = 'json')

        self.assertEqual(400, response.status_code)


class UserLoginAPIViewTestCase(APITestCase):
    url = '/user/auth/'

    def setUp(self):
        self.username = "testuser"
        self.password = "testpassword"
        self.user = CustomUser.objects.create_user(self.username, self.password)

    def test_authentication_without_password(self):
        response = self.client.post(
            self.url, 
            data = {"username" : "benis"},
            format = 'json'
        )

        self.assertEqual(400, response.status_code)

    def test_authentication_with_wrong_password(self):
        response = self.client.post(
            self.url, 
            data = {"username": self.username, "password": "m3m35"},
            format = 'json'
        )

        self.assertEqual(400, response.status_code)

    # depricated, 'cause https://www.django-rest-framework.org/api-guide/testing/ advices just to use force_authentication()
    '''
    def test_authentication_with_valid_password(self):
        response = self.client.post(
            self.url, 
            data = {'username' : self.username, 'password': self.password},
            format = 'json'
        )

        self.assertEqual(200, response.status_code)
    '''

'''
class UserTokenAPIViewTestCase(APITestCase):
    def url(self, key):
        return reverse("authorization", kwargs={"key": key})

    def setUp(self):
        self.username = "Pepe The Frog"
        self.password = "p3p3m3m35"
        self.user = CustomUser.objects.create_user(self.username, self.password)
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

        self.user_2 = CustomUser.objects.create_user(username = "Benis", password = "superbenis")
        self.token_2 = Token.objects.create(user=self.user_2)

    def tearDown(self):
        self.user.delete()
        self.token.delete()
        self.user_2.delete()
        self.token_2.delete()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + self.token.key)

    def test_delete_by_key(self):
        response = self.client.delete(self.url(self.token.key))
        self.assertEqual(204, response.status_code)
        self.assertFalse(Token.objects.filter(key=self.token.key).exists())

    def test_delete_current(self):
        response = self.client.delete(self.url('current'))
        self.assertEqual(204, response.status_code)
        self.assertFalse(Token.objects.filter(key=self.token.key).exists())

    def test_delete_unauthorized(self):
        response = self.client.delete(self.url(self.token_2.key))
        self.assertEqual(404, response.status_code)
        self.assertTrue(Token.objects.filter(key=self.token_2.key).exists())

    def test_get(self):
        # Test that unauthorized access returns 404
        response = self.client.get(self.url(self.token_2.key))
        self.assertEqual(404, response.status_code)

        for key in [self.token.key, 'current']:
            response = self.client.get(self.url(key))
            self.assertEqual(200, response.status_code)
            self.assertEqual(self.token.key, response.data['auth_token'])
            self.assertIn('created', response.data)
'''