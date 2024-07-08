from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from api.models import Organisation

User = get_user_model()

class RegisterTests(APITestCase):
	def setUp(self):
		self.register_url = reverse('register')

	def test_register_user_successfully_with_default_organisation(self):
		data = {
			"email": "john.doe@example.com",
			"password": "password123",
			"first_name": "John",
			"last_name": "Doe",
			"phone": "1234567890"
		}

		response = self.client.post(self.register_url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response.data['status'], 'success')
		self.assertIn('accessToken', response.data['data'])

		user = User.objects.get(email="john.doe@example.com")
		self.assertIsNotNone(user)
		org = Organisation.objects.get(owner=user)
		self.assertEqual(org.name, "John's Organisation")


	def test_login_user_successfully(self):

		user_data = {
			"email": "jane.doe@example.com",
			"password": "password123",
			"first_name": "Jane",
			"last_name": "Doe",
			"phone": "1234567890"
		}
		self.client.post(self.register_url, user_data, format='json')

		login_data = {
			"email": "jane.doe@example.com",
			"password": "password123"
		}
		response = self.client.post(reverse('token_obtain_pair'), login_data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertIn('access', response.data)

	def test_fail_if_required_fields_are_missing(self):
		data = {
			"email": "missing.fields@example.com",
			"password": "password123",
			"last_name": "LastName"
		}

		response = self.client.post(self.register_url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
		self.assertIn('first_name', response.data)

		data = {
			"email": "missing.fields@example.com",
			"password": "password123",
			"first_name": "FirstName"
		}

		response = self.client.post(self.register_url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
		self.assertIn('last_name', response.data)

		data = {
			"email": "missing.fields@example.com",
			"first_name": "FirstName",
			"last_name": "LastName"
		}

		response = self.client.post(self.register_url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
		self.assertIn('password', response.data)

		data = {
			"first_name": "FirstName",
			"last_name": "LastName",
			"password": "Pasword123"
		}

		response = self.client.post(self.register_url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
		self.assertIn('email', response.data)


	def test_fail_if_duplicate_email_or_userid(self):
		data1 = {
			"email": "duplicate@example.com",
			"password": "password123",
			"first_name": "First",
			"last_name": "User",
			"phone": "1234567890"
		}

		data2 = {
			"email": "duplicate@example.com",
			"password": "password123",
			"first_name": "Second",
			"last_name": "User",
			"phone": "1234567890"
		}

		self.client.post(self.register_url, data1, format='json')
		response = self.client.post(self.register_url, data2, format='json')
		self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

		self.assertIn('email', response.data)
		