from django.db import models
import uuid
class Client(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type_client = models.IntegerField(default=0) # 1 client bar, 2 livreur
    nom = models.CharField(max_length=255)
    adresse = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)
    mail = models.EmailField(null=True, blank=True)
    qte_consignation_ca = models.IntegerField(default=0,null=True,blank=True)
    qte_consignation_btle = models.IntegerField(default=0,null=True,blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.nom