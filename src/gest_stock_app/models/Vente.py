from django.db import models,transaction
import uuid
import random
import string
import datetime
from gest_stock_app.models.Client import Client

class Vente(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=20, unique=True, null=True, blank=True,)
    type_vente = models.IntegerField(default=0) # 1 client bar, 2 livreur
    date = models.DateField()
    #total = models.DecimalField(max_digits=10, decimal_places=2)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True,blank=True)
    montant_percu = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True, default=0) #pas utiliser
    remise = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True) 
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.client}-{self.date}"

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_order_code()
        super(Vente, self).save(*args, **kwargs)
    
    @transaction.atomic
    def delete(self ):
        if self.is_deleted is True:
            return
        self.is_deleted = True
        self.save()
        self.detailVente.update(is_deleted=True)

    def generate_order_code(self):
        #return f'VTE_{self.generate_random_string()}'
        today = datetime.datetime.now().strftime('%d%m%y')
        #recuperer le nombre de vente du jour
        nbre_vente = Vente.objects.filter(date=datetime.date.today(),is_deleted=False).count()+1
        code = f'VTE_{today}_0{nbre_vente}'
        
        # Boucle pour garantir l'unicité du code
        while Vente.objects.filter(code=code).exists():
            nbre_vente += 1
            code = f'VTE_{today}_0{nbre_vente}'
        
        return code

    def generate_random_string(self, length=8):
        """ Génère une chaîne alphanumérique avec la data du jour + 00X x un nombre incrementable pour chaque jour """
        characters = string.ascii_uppercase + string.digits
        return ''.join(random.choices(characters, k=length))