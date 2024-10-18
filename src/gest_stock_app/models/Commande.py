from django.db import models,transaction

from gest_stock_app.models.Distributeur import Distributeur
import uuid
import random
import string
class Commande(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=255,blank=True,null=True)
    date = models.DateField()
    mt_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    distributeur = models.ForeignKey(Distributeur, on_delete=models.CASCADE, null=True, blank=True)
    frais_transport = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    type_transport = models.CharField(max_length=255, null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True) 
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.fournisseur}-{self.date}"

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_order_code()
        super(Commande, self).save(*args, **kwargs)
    
    #transaction atomic pour suppression commande et detailCommande
    @transaction.atomic
    def delete(self ):
        if self.is_deleted is True:
            return
        self.is_deleted = True
        self.save()
        self.detailCommande.update(is_deleted=True)

    def generate_order_code(self):
        return f'CMD_{self.generate_random_string()}'

    def generate_random_string(self, length=8):
        """ Génère une chaîne alphanumérique aléatoire """
        characters = string.ascii_uppercase + string.digits
        return ''.join(random.choices(characters, k=length))

   