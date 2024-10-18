from django.db import models

from gest_stock_app.models.Client import Client
from gest_stock_app.models.Produit import Produit
from gest_stock_app.models.TypeCasier import TypeCasier
import uuid
class Consignation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    libelle = models.CharField(max_length=255)
    type_consignation = models.IntegerField(default=0) # 1 emprunt, 2 retour
    type_garantie = models.IntegerField(default=0,null=True,blank=True) # 1 argent 2 piece
    garantie = models.TextField(null=True,blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE,related_name='consignation')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True) 
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.libelle} ({self.qte_casier} casiers)"
    
    
        