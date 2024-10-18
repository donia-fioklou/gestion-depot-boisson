from django.db import models

from gest_stock_app.models.Vente import Vente
import uuid
class Facture(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference = models.CharField(max_length=255)
    vente = models.ForeignKey(Vente, on_delete=models.CASCADE)
    file_path = models.FileField(upload_to='factures/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)


    def __str__(self):
        return f"Facture {self.reference} pour la vente {self.vente.code}"
