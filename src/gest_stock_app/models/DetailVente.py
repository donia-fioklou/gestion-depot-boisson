from django.db import models

from gest_stock_app.models.Produit import Produit
#from gest_stock_app.models.TypeCasier import TypeCasier
from gest_stock_app.models.Vente import Vente
import uuid

class DetailVente(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vente = models.ForeignKey(Vente, on_delete=models.CASCADE,related_name="detailVente")
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    #type_casier = models.ForeignKey(TypeCasier, on_delete=models.CASCADE)
    qte_casier = models.FloatField(default=0.0)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True) 
    is_deleted = models.BooleanField(default=False)

    
    def __str__(self):
        return f"{self.qte_casier} casiers de {self.produit.nom} pour la vente {self.vente.code}"
