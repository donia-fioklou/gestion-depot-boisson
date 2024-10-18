from django.db import models

from gest_stock_app.models.Commande import Commande
from gest_stock_app.models.Produit import Produit
#from gest_stock_app.models.TypeCasier import TypeCasier
import uuid

class DetailCommande(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE,related_name='detailCommande')
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    #type_casier = models.ForeignKey(TypeCasier, on_delete=models.CASCADE)
    qte_casier = models.IntegerField()
    pu = models.DecimalField(max_digits=10, decimal_places=2) # pu casier
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True) 
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.qte_casier} casiers de {self.produit.nom} pour la commande {self.commande.code}"
    