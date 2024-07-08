from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Organisation
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings
from datetime import timedelta
import pdb


CustomerUser = get_user_model()

class TokenTestCase(TestCase):

	def setUp(self):
		self.user = CustomerUser.objects.create_user(
			email = 'testuser@example.com',
			password = 'testpassword',
			first_name = 'Test',
			phone = '08215744603',
			last_name = 'User'
		)

	def test_token_generation(self):
		refresh = RefreshToken.for_user(self.user)

		self.assertIsNotNone(refresh)
		self.assertIsNotNone(refresh.access_token)

	def test_token_expiration(self):
		refresh = RefreshToken.for_user(self.user)
		access_token = refresh.access_token

		expected_expiry = (access_token.current_time + api_settings.ACCESS_TOKEN_LIFETIME).timestamp()

		actual_expiry = access_token.payload['exp']

		delta = timedelta(seconds=5).total_seconds()

		self.assertAlmostEqual(expected_expiry, actual_expiry, delta=delta)

	def test_user_details_in_token(self):
		refresh = RefreshToken.for_user(self.user)
		access_token = refresh.access_token

		

		self.assertEqual(access_token.payload['user_id'], str(self.user.userId))



class OrganisationAccessTestCase(TestCase):

	def setUp(self):
		self.user1 = CustomerUser.objects.create_user(
			email='user1@example.com',
			password='password123',
			first_name='User',
			last_name='One',
			phone='08182828282'
		)
		self.user2 = CustomerUser.objects.create_user(
			email='user2@example.com',
			password='password123',
			first_name='User',
			last_name='Two',
			phone='08182828382'
		)

		self.org1 = Organisation.objects.create(
			name="Org One",
			description="First Organisation",
			owner=self.user1
		)
		self.org1.users.add(self.user1)

		self.org2 = Organisation.objects.create(
			name="Org Two",
			description="Second Organisation",
			owner=self.user2
		)
		self.org2.users.add(self.user2)

		self.client = APIClient()

	def test_user1_cannot_access_org2(self):

		self.client.force_authenticate(user=self.user1)

		url = reverse('organisation-detail', args=[self.org2.orgId])
		response = self.client.get(url)

		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

	def test_user2_cannot_access_org1(self):
		self.client.force_authenticate(user=self.user2)

		url = reverse('organisation-detail', args=[self.org1.orgId])
		response = self.client.get(url)

		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)