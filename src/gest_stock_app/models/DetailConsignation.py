from django.db import models
import uuid

from gest_stock_app.models.TypeCasier import TypeCasier
from gest_stock_app.models.Consignation import Consignation
class DetailConsignation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    consignation = models.ForeignKey(Consignation, on_delete=models.CASCADE,related_name="detailConsignation")
    type_casier  = models.ForeignKey(TypeCasier, on_delete=models.CASCADE)
    qte_casier = models.FloatField(default=0.0)
    is_deleted = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True) 