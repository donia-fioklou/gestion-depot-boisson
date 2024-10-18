from django.contrib import admin
from gest_stock_app.models.Client import Client
from gest_stock_app.models.Commande import Commande
from gest_stock_app.models.Consignation import Consignation
from gest_stock_app.models.Defaut import Defaut
from gest_stock_app.models.DetailCommande import DetailCommande
from gest_stock_app.models.DetailVente import DetailVente
from gest_stock_app.models.Facture import Facture
from gest_stock_app.models.Fournisseur import Fournisseur
from gest_stock_app.models.Produit import Produit
from gest_stock_app.models.TypeCasier import TypeCasier
from gest_stock_app.models.Vente import Vente
from gest_stock_app.models.HistoriqueStock import HistoriqueStock

# Register your models here.
admin.site.register(Client)
admin.site.register(Commande)
admin.site.register(Consignation)
admin.site.register(Defaut)
admin.site.register(DetailCommande)
admin.site.register(DetailVente)
admin.site.register(Facture)
admin.site.register(Fournisseur)
admin.site.register(Produit)
admin.site.register(TypeCasier)
admin.site.register(Vente)
admin.site.register(HistoriqueStock)
