from django.test import TestCase, Client
from django.urls import reverse
import json

class YourViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_view(self):
        response = self.client.post(reverse('login'), {'username': 'manogna7', 'password': 'abc12345'})
        self.assertEqual(response.status_code, 302)  # Assert redirect status code

    def test_dashboard_view(self):
        # Simulate a logged-in user session
        self.client.login(username='manogna7', password='abc12345')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)  # Assert successful response

    def test_registration_view(self):
        response = self.client.get(reverse('registration'))
        self.assertEqual(response.status_code, 200)  # Assert successful response

    def test_check_username_availability(self):
        response = self.client.post(reverse('check_username_availability'), json.dumps({'username': 'manogna7'}), content_type='application/json')
        data = json.loads(response.content)
        self.assertTrue('is_taken' in data)  # Assert response contains 'is_taken' key

    # Add more test methods for other views as needed
