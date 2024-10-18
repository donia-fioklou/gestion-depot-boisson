from django.db import models
#from django.contrib.auth.models import User  
from django.conf import settings
from gest_stock_app.models import Produit
User = settings.AUTH_USER_MODEL

class HistoriqueStock(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    qte_change = models.IntegerField()  # Quantité ajoutée ou retirée
    mouvement_type = models.CharField(max_length=255)  # Type de mouvement (par ex. "commande", "vente")
    utilisateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_mouvement = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Produit: {self.produit.nom}, Changement: {self.qte_change}, Type: {self.mouvement_type}, Date: {self.date_mouvement}"
