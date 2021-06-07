from django.test import TestCase
from django.contrib.auth.models import User, Group
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from flower_app.models.People.Membre import Membre
from flower_app.models.Poste import Poste

class ControllersMembresTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        user = User.objects.create_user(username='test_username', password='test_password')
        role_ca_group = Group.objects.create(name='ROLE_CA')
        role_admin_group = Group.objects.create(name='ROLE_ADMIN')
        role_ca_group.user_set.add(user)
        role_admin_group.user_set.add(user)
        self.client.login(username='test_username', password='test_password')

        Membre.objects.create(id=1, promotion="2021", birth_date="1998-01-01")
        Membre.objects.create(id=2, promotion="2020", birth_date="1997-01-01")

        Poste.objects.create(id=1, name='name', name_feminine='name_feminine')

    def test_getMembres(self):
        request = self.client.get(
            '/api/membres/'
        )
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.data), 2)

    def test_addMembres(self):
        newUser = {
                'lastname': 'lastname',
                'firstname': 'firstname',
                'gender': 'M',
                'email_junior': 'firstname.lastname@test.com',
                'mobile': '',
                'address': 'Test',
                'postcode': '0',
                'town': 'TEST',
                'country': 'France',
                'nationality': 'français',
                'birth_place': 'France',
                'email': 'firstname.lastname@test.com',
                'promotion': 2021,
                'birth_date': '1998-01-01',
                'poste': 1,
                'user': None
            }
        request = self.client.post(
            '/api/membres/',
            newUser,
            format='json'
        )
        newUser['id'] = request.data['id']
        newUser['poste'] = { 
            'id': 1,
            'name': 'name',
            'name_feminine': 'name_feminine',
            'subordinates': []
        }
        
        self.assertEqual(request.status_code, 201)
        self.assertDictEqual(request.data, newUser)
        self.assertEqual(Membre.objects.count(), 3)

    def test_getMembreById(self):
        request = self.client.get(
            '/api/membres/2/'
        )
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data['promotion'], 2020)
        self.assertEqual(request.data['birth_date'], "1997-01-01")

    def test_patchMembreById(self):
        request = self.client.patch(
            '/api/membres/2/',
            {
                'promotion': 1990,
                'poste': 1
            },
            format='json'
        )
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data['promotion'], 1990)
        self.assertEqual(request.data['birth_date'], "1997-01-01")

    def test_updateMembreById(self):
        updatedUser = {
            'id': 2,
            'lastname': 'lastname',
            'firstname': 'firstname',
            'gender': 'M',
            'email_junior': 'firstname.lastname@test.com',
            'mobile': '',
            'address': 'Test',
            'postcode': '0',
            'town': 'TEST',
            'country': 'France',
            'nationality': 'français',
            'birth_place': 'France',
            'email': 'firstname.lastname@test.com',
            'promotion': 2003,
            'birth_date': '1980-01-01',
            'poste': 1,
            'user': None
        }
        request = self.client.put(
            '/api/membres/2/',
            updatedUser,
            format='json'
        )
        updatedUser['poste'] = { 
            'id': 1,
            'name': 'name',
            'name_feminine': 'name_feminine',
            'subordinates': []
        }
        self.assertEqual(request.status_code, 200)
        self.assertDictEqual(request.data, updatedUser)
