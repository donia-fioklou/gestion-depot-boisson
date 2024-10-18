from django.db import models
import uuid

from gest_stock_app.models.TypeCasier import TypeCasier
from gest_stock_app.models.Fournisseur import Fournisseur
class Produit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type_casier = models.ForeignKey(TypeCasier, on_delete=models.CASCADE,blank=True,null=True)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE,blank=True,null=True)
    nom = models.CharField(max_length=255)
    pu_bouteille = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    pu_casier = models.DecimalField(max_digits=10, decimal_places=2)
    qte_casier = models.FloatField(default=0.0)
    qte_seuil = models.FloatField(default=0.0,null=True, blank=True)
    #volume = models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True)
    prix_achat_casier = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,default=0)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True) 
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.fournisseur}-{self.nom}"