from django.test import TestCase
from django.contrib.auth.models import User, Group
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

class ControllersAccountTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        user = User.objects.create_user(username='test_username', password='test_password')
        role_ca_group = Group.objects.create(name='ROLE_CA')
        role_ca_group.user_set.add(user)

    def test_accounts_accepted(self):
        request = self.client.post(
            '/api/accounts/login',
            {'username': 'test_username', 'password': 'test_password'}
        )
        self.assertEqual(request.status_code, 202)

    def test_accounts_bad_password(self):
        request = self.client.post(
            '/api/accounts/login',
            {'username': 'test_username', 'password': 'bad_password'}
        )
        self.assertEqual(request.status_code, 401)

    def test_accounts_bad_username(self):
        request = self.client.post(
            '/api/accounts/login',
            {'username': 'bad_username', 'password': 'bad_password'}
        )
        self.assertEqual(request.status_code, 401)

    def test_logout(self):
        '''
        Login, test if the token is valid, logout and test if the token is invalid
        '''
        requestLogin = self.client.post(
            '/api/accounts/login',
            {'username': 'test_username', 'password': 'test_password'}
        )
        csrftoken = requestLogin.cookies['csrftoken']

        requestMembreOK = self.client.get(
            '/api/membres/',
            headers={'X-CSRFToken': csrftoken}
        )

        requestLogout = self.client.get(
            '/api/accounts/logout',
            headers={'X-CSRFToken': csrftoken}
        )

        requestMembreLoggedOut = self.client.get(
            '/api/membres/',
            headers={'X-CSRFToken': csrftoken}
        )

        self.assertEqual(requestMembreOK.status_code, 200)
        self.assertEqual(requestLogout.status_code, 202)
        self.assertEqual(requestMembreLoggedOut.status_code, 403)