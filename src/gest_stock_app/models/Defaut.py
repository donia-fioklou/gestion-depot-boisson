from django.db import models

from gest_stock_app.models.Commande import Commande
from gest_stock_app.models.Produit import Produit
import uuid
class Defaut(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    libelle = models.CharField(max_length=100)
    description = models.TextField()
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    nbre_bouteille = models.IntegerField()
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True) 
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Défaut: {self.libelle} ({self.nbre_bouteille} bouteilles)"