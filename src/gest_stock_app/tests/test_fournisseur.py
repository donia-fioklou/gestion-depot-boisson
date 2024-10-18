from django.test import TestCase

from gest_stock_app.models.Fournisseur import Fournisseur


class FournisseurModelTestCase(TestCase):
    
    def setUp(self):
        self.fournisseur = Fournisseur.objects.create(
            nom="Fournisseur Test",
            adresse="Adresse de test",
            telephone="1234567890",
            mail="test@example.com"
        )

    def test_fournisseur_creation(self):
        fournisseur = Fournisseur.objects.get(nom="Fournisseur Test")
        self.assertEqual(fournisseur.nom, "Fournisseur Test")
        self.assertEqual(fournisseur.adresse, "Adresse de test")
        self.assertEqual(fournisseur.telephone, "1234567890")
        self.assertEqual(fournisseur.mail, "test@example.com")

    
