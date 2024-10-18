from django.db import models
import uuid
class Fournisseur(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=255)
    adresse = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)
    mail = models.EmailField(null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True) 
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.nom