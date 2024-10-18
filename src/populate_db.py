import os
import django
# Configurer Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bkb_boisson_back.settings')
django.setup()

from faker import Faker
from gest_stock_app.models.Client import Client
from gest_stock_app.models.Produit import Produit
from gest_stock_app.models.Commande import Commande
from gest_stock_app.models.Consignation import Consignation
from gest_stock_app.models.Defaut import Defaut
from gest_stock_app.models.Facture import Facture
from gest_stock_app.models.DetailCommande import DetailCommande
from gest_stock_app.models.DetailVente import DetailVente
from gest_stock_app.models.Vente import Vente
from gest_stock_app.models.Fournisseur import Fournisseur
from gest_stock_app.models.TypeCasier import TypeCasier
from gest_stock_app.models.HistoriqueStock import HistoriqueStock




# Initialiser Faker
fake = Faker()

def populate():
    # Créer des clients
    clients = []
    for _ in range(10):
        client = Client.objects.create(
            nom=fake.name(),
            adresse=fake.address(),
            telephone=fake.phone_number(),
            mail=fake.email(),
        )
        clients.append(client)
    
    # Créer des fournisseurs
    fournisseurs = []
    for _ in range(5):
        fournisseur = Fournisseur.objects.create(
            nom=fake.company(),
            adresse=fake.address(),
            telephone=fake.phone_number(),
            mail=fake.email(),
        )
        fournisseurs.append(fournisseur)
    
    # Créer des types de casiers
    types_casier = []
    for _ in range(3):
        type_casier = TypeCasier.objects.create(
            taille=fake.random_number(digits=2),
        )
        types_casier.append(type_casier)

    # Créer des produits
    produits = []
    for _ in range(20):
        produit = Produit.objects.create(
            nom=fake.word(),
            type_casier=fake.random_element(types_casier),
            fournisseur=fake.random_element(fournisseurs),
            pu_casier=fake.random_number(digits=3),
            prix_achat_casier=fake.random_number(digits=3),
            pu_bouteille=fake.random_number(digits=2),
        )
        produits.append(produit)

    # Créer des commandes
    commandes = []
    for _ in range(10):
        commande = Commande.objects.create(
            date=fake.date_this_year(),
            fournisseur=fake.random_element(fournisseurs),
            frais_transport=fake.random_number(digits=2),
        )
        commandes.append(commande)

    # Créer des détails de commande
    for commande in commandes:
        for _ in range(3):
            DetailCommande.objects.create(
                commande=commande,
                produit=fake.random_element(produits),
                qte_casier=fake.random_number(digits=2),
                pu=fake.random_number(digits=3),
            )
    
    # Créer des consignations
    for _ in range(5):
        Consignation.objects.create(
            libelle=fake.word(),
            #type_casier=fake.random_element(types_casier),
            type_consignation=fake.random_int(min=0, max=1),
            type_garantie=fake.random_int(min=0, max=1),
            qte_casier=fake.random_number(digits=2),
            qte_bouteille=fake.random_number(digits=2),
            garantie=fake.text(),
            client=fake.random_element(clients),
        )

    # Créer des défauts
    for _ in range(5):
        Defaut.objects.create(
            libelle=fake.word(),
            description=fake.text(),
            commande=fake.random_element(commandes),
            produit=fake.random_element(produits),
            nbre_bouteille=fake.random_number(digits=2),
        )

    # Créer des ventes
    ventes = []
    for _ in range(10):
        vente = Vente.objects.create(
            date=fake.date_this_year(),
            client=fake.random_element(clients),
        )
        ventes.append(vente)
    
    # Créer des détails de vente
    for vente in ventes:
        for _ in range(3):
            DetailVente.objects.create(
                vente=vente,
                produit=fake.random_element(produits),
                qte_casier=fake.random_number(digits=2),
            )
    
    # Créer des factures
    for vente in ventes:
        Facture.objects.create(
            reference=fake.uuid4(),
            vente=vente,
            file_path=fake.file_path(),
        )

if __name__ == "__main__":
    populate()
