from django.test import TestCase
from django.contrib.auth.models import User, Group
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from flower_app.models.People.Prospect import Prospect
from flower_app.models.People.Employe import Employe

class ControllersProspectsTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        user = User.objects.create_user(username='test_username', password='test_password')
        role_ca_group = Group.objects.create(name='ROLE_CA')
        role_ca_group.user_set.add(user)
        self.client.login(username='test_username', password='test_password')

        self.prospect1 = Prospect.objects.create(id=1, name="Prospect 1", address="Adresse prospect 1", postcode="35700", town="Rennes")
        Prospect.objects.create(id=2, name="Prospect 2", address="Adresse prospect 2", postcode="44000", town="Nantes")
        Employe.objects.create(id=1, prospect=self.prospect1, firstname='test_firstname', lastname='test_lastname')

    def test_getProspect(self):
        request = self.client.get(
            '/api/prospects/'
        )
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.data), 2)

    def test_addProspect(self):
        newProspect = {
            'name': 'Prospect 3',
            'address': 'Adresse prospect 3',
            'postcode': '35170',
            'town': 'Chaton'
        }
        request = self.client.post(
            '/api/prospects/',
            newProspect
        )
        newProspect['id'] = request.data['id']
        self.assertEqual(request.status_code, 201)
        self.assertDictEqual(request.data, newProspect)
        self.assertEqual(Prospect.objects.count(), 3)

    def test_getProspectsById(self):
        request = self.client.get(
            '/api/prospects/2/'
        )
        expectedValues = { 'id': 2, 'name':"Prospect 2", 'address':"Adresse prospect 2", 'postcode':"44000", 'town':"Nantes"}
        self.assertEqual(request.status_code, 200)
        self.assertDictEqual(request.data, expectedValues)

    def test_patchProspectById(self):
        request = self.client.patch(
            '/api/prospects/2/',
            {
                'name': 'New prospect name'
            }
        )
        expectedValues = { 'id': 2, 'name': 'New prospect name', 'address': "Adresse prospect 2", 'postcode': "44000", 'town': "Nantes"}
        self.assertEqual(request.status_code, 200)
        self.assertDictEqual(request.data, expectedValues)

    def test_updateProspectById(self):
        updatedUser = {
            'id': 2,
            'name': 'New prospect name',
            'address': 'New adresse prospect 2',
            'postcode': '44000',
            'town': 'Nantes'
        }

        request = self.client.put(
            '/api/prospects/2/',
            updatedUser
        )
        self.assertEqual(request.status_code, 200)
        self.assertDictEqual(request.data, updatedUser)

    def test_getEmploye(self):
        request = self.client.get(
            '/api/prospects/1/employes/1/'
        )
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data['firstname'], 'test_firstname')
        self.assertEqual(request.data['lastname'], 'test_lastname')

    def test_putEmploye(self):
        updatedEmploye = {
            'id': 1,
            'prospect': 1,
            'firstname': 'test_new_firstname',
            'lastname': 'test_new_lastname',
            'gender': 'N/A',
            'email': 'test@example.com',
            'position': 'test_position'
        }
        request = self.client.put(
            '/api/prospects/1/employes/1/',
            updatedEmploye
        )
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data['firstname'], 'test_new_firstname')
        self.assertEqual(request.data['lastname'], 'test_new_lastname')

    def test_patchEmploye(self):
        updatedEmploye = {
            'id': 1,
            'prospect': 1,
            'firstname': 'test_new_firstname'
        }
        request = self.client.patch(
            '/api/prospects/1/employes/1/',
            updatedEmploye
        )
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data['firstname'], 'test_new_firstname')
        self.assertEqual(request.data['lastname'], 'test_lastname')

    def test_deleteEmploye(self):
        self.assertEqual(Prospect.objects.get(id=1).employe_set.count(), 1)
        request = self.client.delete(
            '/api/prospects/1/employes/1/',
            { 'id': 1 }
        )
        self.assertEqual(request.status_code, 204)
        self.assertEqual(Prospect.objects.get(id=1).employe_set.count(), 0)