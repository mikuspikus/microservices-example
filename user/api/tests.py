# import json

# from rest_framework.test import APIClient, force_authenticate, APITestCase
# from rest_framework.authtoken.models import Token

# from django.urls import reverse

# from .models import CustomUser

# class UserRegistrationAPIViewTestCase(APITestCase):
#     url = '/user/register/'

#     def test_user_registration(self):
#         user_data = {
#             "username": "testuser",
#             "password": "123123",
#             "confirm_password": "123123"
#         }

#         response = self.client.post(self.url, user_data, format = 'json')

#         self.assertEqual(201, response.status_code)

#     def test_unique_username_validation(self):
#         user_data_1 = {
#             "username": "testuser",
#             "password": "123123",
#             "confirm_password": "123123"
#         }

#         response = self.client.post(self.url, user_data_1, format = 'json')

#         self.assertEqual(201, response.status_code)

#         user_data_2 = {
#             "username": "testuser",
#             "password": "123123",
#             "confirm_password": "123123"
#         }

#         response = self.client.post(self.url, user_data_2, format = 'json')

#         self.assertEqual(400, response.status_code)


# class UserLoginAPIViewTestCase(APITestCase):
#     url = '/user/auth/'

#     def setUp(self):
#         self.username = "testuser"
#         self.password = "testpassword"
#         self.user = CustomUser.objects.create_user(self.username, self.password)

#     def test_authentication_without_password(self):
#         response = self.client.post(
#             self.url, 
#             data = {"username" : "benis"},
#             format = 'json'
#         )

#         self.assertEqual(400, response.status_code)

#     def test_authentication_with_wrong_password(self):
#         response = self.client.post(
#             self.url, 
#             data = {"username": self.username, "password": "m3m35"},
#             format = 'json'
#         )

#         self.assertEqual(400, response.status_code)

#     # depricated, 'cause https://www.django-rest-framework.org/api-guide/testing/ advices just to use force_authentication()
