from django.test import TestCase
from flower_app.models.People.Realisateur import Realisateur, RealisateurComment
from flower_app.models.People.Membre import Membre
from flower_app.models.People.Prospect import Prospect
from flower_app.models.People.Employe import Employe
from flower_app.models.Etude import Etude
from flower_app.models.Prospection import ContactWay

class AnonymiseTest(TestCase):
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
        self.assertEqual(anonymisedProspect.name, "xxxxx")
        self.assertEqual(anonymisedProspect.address, "xxxxx")
        self.assertEqual(anonymisedProspect.postcode, "xxxxx")
        self.assertEqual(anonymisedProspect.town, "xxxxx")
        self.assertEqual(anonymisedProspect.contactWay.all()[0].contactWay, "xxxxx")

        anonymisedEmploye = anonymisedProspect.employe_set.all()[0]
        self.assertEqual(anonymisedEmploye.lastname, "xxxxx")
        self.assertEqual(anonymisedEmploye.firstname, "xxxxx")
        self.assertEqual(anonymisedEmploye.gender, "xxxxx")
        self.assertEqual(anonymisedEmploye.mobile, "xxxxx")
        self.assertEqual(anonymisedEmploye.email, "xxxxx")

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
        self.assertEqual(anonymisedMembre.lastname, "xxxxx")
        self.assertEqual(anonymisedMembre.firstname, "xxxxx")
        self.assertEqual(anonymisedMembre.gender, "xxxxx")
        self.assertEqual(anonymisedMembre.mobile, "xxxxx")
        self.assertEqual(anonymisedMembre.email, "xxxxx")
        self.assertEqual(anonymisedMembre.user, None)
        self.assertEqual(anonymisedMembre.promotion, -1)
        self.assertEqual(anonymisedMembre.email_junior, "xxxxx")
        self.assertEqual(anonymisedMembre.address, "xxxxx")
        self.assertEqual(anonymisedMembre.postcode, "xxxxx")
        self.assertEqual(anonymisedMembre.town, "xxxxx")
        self.assertEqual(anonymisedMembre.country, "xxxxx")
        self.assertEqual(anonymisedMembre.nationality, "xxxxx")
        self.assertEqual(anonymisedMembre.birth_date.isoformat(), "1970-01-01")
        self.assertEqual(anonymisedMembre.birth_place, "xxxxx")

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
        self.assertEqual(anonymisedRealisateur.lastname, "xxxxx")
        self.assertEqual(anonymisedRealisateur.firstname, "xxxxx")
        self.assertEqual(anonymisedRealisateur.gender, "xxxxx")
        self.assertEqual(anonymisedRealisateur.mobile, "xxxxx")
        self.assertEqual(anonymisedRealisateur.email, "xxxxx")
        self.assertEqual(anonymisedRealisateur.user, None)
        self.assertEqual(anonymisedRealisateur.promotion, -1)
        self.assertEqual(anonymisedRealisateur.email_insa, "xxxxx")
        self.assertEqual(anonymisedRealisateur.address, "xxxxx")
        self.assertEqual(anonymisedRealisateur.postcode, "xxxxx")
        self.assertEqual(anonymisedRealisateur.town, "xxxxx")
        self.assertEqual(anonymisedRealisateur.country, "xxxxx")
        self.assertEqual(anonymisedRealisateur.nationality, "xxxxx")
        self.assertEqual(anonymisedRealisateur.birth_date.isoformat(), "1970-01-01")
        self.assertEqual(anonymisedRealisateur.birth_place, "xxxxx")
        self.assertEqual(anonymisedRealisateur.comments.all()[0].content, "xxxxx")