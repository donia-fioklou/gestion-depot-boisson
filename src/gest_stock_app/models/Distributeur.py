from django.db import models
import uuid

from gest_stock_app.models.Fournisseur import Fournisseur

class Distributeur(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE)
    nom = models.CharField(max_length=255)
    adresse = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)
    mail = models.EmailField(null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True) 
    is_deleted = models.BooleanField(default=False)