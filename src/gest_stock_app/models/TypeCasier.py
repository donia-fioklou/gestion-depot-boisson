from django.db import models
import uuid

class TypeCasier(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    taille = models.PositiveIntegerField(default=0)
    #tauxReduction = models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True) 
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Taille: {self.taille} bouteilles"
