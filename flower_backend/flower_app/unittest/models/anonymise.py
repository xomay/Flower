from django.conf import settings
from django.test import TestCase

from flower_app.models.People.Realisateur import Realisateur, RealisateurComment
from flower_app.models.People.Membre import Membre
from flower_app.models.People.Prospect import Prospect
from flower_app.models.People.Employe import Employe
from flower_app.models.Etude import Etude
from flower_app.models.Prospection import ContactWay

class AnonymiseTest(TestCase):

    def setUp(self):
        self.assertEqual(settings.ANONYMISATION_STRING, 'xxxxx')
        self.assertEqual(settings.ANONYMISATION_DATE, '1970-01-01')
        self.assertEqual(settings.ANONYMISATION_INTEGER, -1)

    def test_anonymiseProspect(self):
        prospect = Prospect.objects.create(
            id=1,
            name = "test_name",
            address = "test_address",
            postcode = "test_postcode",
            town = "test_town",
        )
        Employe.objects.create(prospect=prospect, position="test_position")
        prospect.contactWay.add(ContactWay.objects.create(contactWay="test_contactWay"))
        prospect.anonymiser()

        anonymisedProspect = Prospect.objects.get(pk=1)
        self.assertEqual(anonymisedProspect.name, settings.ANONYMISATION_STRING)
        self.assertEqual(anonymisedProspect.address, settings.ANONYMISATION_STRING)
        self.assertEqual(anonymisedProspect.postcode, settings.ANONYMISATION_STRING)
        self.assertEqual(anonymisedProspect.town, settings.ANONYMISATION_STRING)
        self.assertEqual(anonymisedProspect.contactWay.all()[0].contactWay, settings.ANONYMISATION_STRING)

        anonymisedEmploye = anonymisedProspect.employe_set.all()[0]
        self.assertEqual(anonymisedEmploye.lastname, settings.ANONYMISATION_STRING)
        self.assertEqual(anonymisedEmploye.firstname, settings.ANONYMISATION_STRING)
        self.assertEqual(anonymisedEmploye.gender, settings.ANONYMISATION_STRING)
        self.assertEqual(anonymisedEmploye.mobile, settings.ANONYMISATION_STRING)
        self.assertEqual(anonymisedEmploye.email, settings.ANONYMISATION_STRING)

    def test_anonymiseMembre(self):
        membre = Membre.objects.create(
            id=1,
            lastname="test_lastname",
            firstname="test_firstname",
            gender="test_gender",
            mobile="test_mobile",
            email="test@example.com",
            promotion=2021,
            email_junior="test@example.com",
            postcode="test_postcode",
            town="test_town",
            country="test_country",
            nationality="test_nationality",
            birth_date="1998-01-01",
            birth_place="test_birthplace"
        )
        membre.anonymiser()
        anonymisedMembre = Membre.objects.get(pk=1)
        self.assertEqual(anonymisedMembre.lastname, settings.ANONYMISATION_STRING)
        self.assertEqual(anonymisedMembre.firstname, settings.ANONYMISATION_STRING)
        self.assertEqual(anonymisedMembre.gender, settings.ANONYMISATION_STRING)
        self.assertEqual(anonymisedMembre.mobile, settings.ANONYMISATION_STRING)
        self.assertEqual(anonymisedMembre.email, settings.ANONYMISATION_STRING)
        self.assertEqual(anonymisedMembre.user, None)
        self.assertEqual(anonymisedMembre.promotion, settings.ANONYMISATION_INTEGER)
        self.assertEqual(anonymisedMembre.email_junior, settings.ANONYMISATION_STRING)
        self.assertEqual(anonymisedMembre.address, settings.ANONYMISATION_STRING)
        self.assertEqual(anonymisedMembre.postcode, settings.ANONYMISATION_STRING)
        self.assertEqual(anonymisedMembre.town, settings.ANONYMISATION_STRING)
        self.assertEqual(anonymisedMembre.country, settings.ANONYMISATION_STRING)
        self.assertEqual(anonymisedMembre.nationality, settings.ANONYMISATION_STRING)
        self.assertEqual(anonymisedMembre.birth_date.isoformat(), settings.ANONYMISATION_DATE)
        self.assertEqual(anonymisedMembre.birth_place, settings.ANONYMISATION_STRING)

    def test_anonymiseRealisateur(self):
        realisateur = Realisateur.objects.create(
            id=1,
            lastname="test_lastname",
            firstname="test_firstname",
            gender="test_gender",
            mobile="test_mobile",
            email="test@example.com",
            promotion=2021,
            email_insa="test@example.com",
            postcode="test_postcode",
            town="test_town",
            country="test_country",
            nationality="test_nationality",
            birth_date="1998-01-01",
            birth_place="test_birthplace"
        )
        prospect = Prospect.objects.create(
            name="test_name",
            address="test_address",
            postcode="test_postcode",
            town="test_town"
        )
        etude = Etude.objects.create(
            mandat=2021,
            number=1,
            name="test_etude",
            confidential=False,
            prospect=prospect
        )
        comment = RealisateurComment.objects.create(
            content="test_content",
            associatedEtude=etude
        )
        realisateur.comments.add(comment)
        realisateur.anonymiser()
        anonymisedRealisateur = Realisateur.objects.get(pk=1)
        self.assertEqual(anonymisedRealisateur.lastname, settings.ANONYMISATION_STRING)
        self.assertEqual(anonymisedRealisateur.firstname, settings.ANONYMISATION_STRING)
        self.assertEqual(anonymisedRealisateur.gender, settings.ANONYMISATION_STRING)
        self.assertEqual(anonymisedRealisateur.mobile, settings.ANONYMISATION_STRING)
        self.assertEqual(anonymisedRealisateur.email, settings.ANONYMISATION_STRING)
        self.assertEqual(anonymisedRealisateur.user, None)
        self.assertEqual(anonymisedRealisateur.promotion, settings.ANONYMISATION_INTEGER)
        self.assertEqual(anonymisedRealisateur.email_insa, settings.ANONYMISATION_STRING)
        self.assertEqual(anonymisedRealisateur.address, settings.ANONYMISATION_STRING)
        self.assertEqual(anonymisedRealisateur.postcode, settings.ANONYMISATION_STRING)
        self.assertEqual(anonymisedRealisateur.town, settings.ANONYMISATION_STRING)
        self.assertEqual(anonymisedRealisateur.country, settings.ANONYMISATION_STRING)
        self.assertEqual(anonymisedRealisateur.nationality, settings.ANONYMISATION_STRING)
        self.assertEqual(anonymisedRealisateur.birth_date.isoformat(), settings.ANONYMISATION_DATE)
        self.assertEqual(anonymisedRealisateur.birth_place, settings.ANONYMISATION_STRING)
        self.assertEqual(anonymisedRealisateur.comments.all()[0].content, settings.ANONYMISATION_STRING)